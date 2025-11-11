import csv, datetime
from pathlib import Path
from pymongo import MongoClient, InsertOne

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "moviedb"

def create_indexes(db):
    db.ratings.create_index([("movieId",1),("ts",-1)])
    db.ratings.create_index([("userId",1),("ts",-1)])
    db.ratings.create_index([("movieId",1),("userId",1)])
    db.movies.create_index([("movieId",1)], unique=True)
    db.movies.create_index([("genres",1)])
    db.users.create_index([("userId",1)], unique=True)
    db.users.create_index([("country",1)])

def load_movies(fp, db):
    if not Path(fp).exists(): return
    ops=[]
    with open(fp, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            genres = [g for g in (row.get("genres") or "").split("|") if g and g!="(no genres listed)"]
            year = int(row["year"]) if row.get("year") else None
            ops.append(InsertOne({"movieId": int(row["movieId"]), "title": row["title"], "year": year, "genres": genres}))
    if ops: db.movies.bulk_write(ops)

def load_ratings(fp, db):
    if not Path(fp).exists(): return
    ops=[]; batch=0
    with open(fp, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            ops.append(InsertOne({
                "userId": int(row["userId"]),
                "movieId": int(row["movieId"]),
                "rating": float(row["rating"]),
                "ts": datetime.datetime.fromtimestamp(int(row["timestamp"]))
            }))
            if len(ops)>=100_000:
                db.ratings.bulk_write(ops); ops=[]; batch+=1
                print(f"Inserted {batch*100_000} ratings...")
    if ops: db.ratings.bulk_write(ops)

def load_users(fp, db):
    if not Path(fp).exists(): return
    ops=[]
    with open(fp, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            prefs = {"genres":[g.strip() for g in (row.get("genres") or "").split("|") if g]}
            age = int(row["age"]) if row.get("age") else None
            join = datetime.datetime.strptime(row["joinDate"], "%Y-%m-%d") if row.get("joinDate") else None
            ops.append(InsertOne({
                "userId": int(row["userId"]),
                "name": row.get("name") or f"user_{row['userId']}",
                "joinDate": join, "country": row.get("country") or None,
                "age": age, "preferences": prefs
            }))
    if ops: db.users.bulk_write(ops)

if __name__ == "__main__":
    cli = MongoClient(MONGO_URI); db = cli[DB_NAME]
    # Always start clean (development safety)
    db.movies.drop()
    db.ratings.drop()
    db.users.drop()

    create_indexes(db)
    load_movies("data/movies.csv", db)
    load_ratings("data/ratings.csv", db)
    load_users("data/users.csv", db)
    print("Done.")

# 🎬 NoSQL_MovieRatings  
**End-to-End NoSQL Database Implementation and Benchmarking**

MongoDB-based data engineering project exploring flexible schema design, CRUD operations, aggregation pipelines, and hybrid SQL/NoSQL performance benchmarking using the **MovieLens** dataset.

---

## 🧠 Overview

This project demonstrates how to:
- Design a **NoSQL schema** for movie ratings (users, movies, ratings).
- Build a **Python + PyMongo loader** for CSV ingestion.
- Run **MongoDB aggregations** for analytics.
- Compare **query latency** and flexibility between MongoDB and PostgreSQL.
- Optionally integrate **Spark** via MongoDB Connector for scalable workflows.

The dataset is derived from [MovieLens](https://grouplens.org/datasets/movielens/) and preprocessed into structured CSVs (`movies.csv`, `ratings.csv`, `users.csv`).

---

## 🏗️ Architecture

```mermaid
flowchart LR
  A[CSV: ratings/movies/users] --> B[Loader (Python + PyMongo)]
  B --> C[(MongoDB)]
  C <--> D[Aggregations (Mongo Pipeline)]
  C <--> E[(Spark Mongo Connector) – optional]
  A --> F[(Postgres baseline – optional)]
  F <--> G[SQL Benchmarks]
  C <--> H[NoSQL Benchmarks]
Components

Python + PyMongo – load data and run aggregations.
MongoDB – main database for NoSQL model.
PostgreSQL – baseline for structured analytical comparison.
Docker Compose – runs MongoDB, Mongo Express, and PostgreSQL locally.
Spark Connector (optional) – future integration for hybrid data processing.
⚙️ Setup
1️⃣ Clone and build
git clone https://github.com/krotov79/02_NoSQL_MovieRatings.git
cd 02_NoSQL_MovieRatings
docker compose up -d

2️⃣ Prepare environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

3️⃣ Download dataset
mkdir -p external
cd external
wget https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
unzip -o ml-latest-small.zip -d ml-latest-small
cd ..

4️⃣ Preprocess MovieLens data
python scripts/prepare_movielens.py


This script generates cleaned CSVs under data/:

movies.csv

ratings.csv

users.csv

💾 Load Data into MongoDB
python src/load_data.py


Sample log:

Inserted 9742 movies...
Inserted 610 users...
Inserted 100000 ratings...
Done.


Quick verification:

python - <<'PY'
from queries import top_movies
print(top_movies(min_votes=50, top_n=10))
PY

🧮 Benchmarking (MongoDB vs PostgreSQL)
Load into PostgreSQL
./scripts/pg_load.sh

Run the benchmark
python src/benchmark_sql_vs_nosql.py


Output:

Mongo top_movies: {'mean_ms': 59.83, 'p95_ms': 61.55}
Postgres top_movies: {'mean_ms': 15.49, 'p95_ms': 12.51}
Mongo user_history: {'mean_ms': 52.11, 'p95_ms': 52.13}
Postgres user_history: {'mean_ms': 8.33, 'p95_ms': 8.3}

📊 Benchmark Results & Discussion
Query Type	MongoDB (ms)	PostgreSQL (ms)	Observation
Top Movies (Aggregation)	mean ≈ 59.83 / p95 ≈ 61.55	mean ≈ 15.49 / p95 ≈ 12.51	SQL’s query planner optimizes aggregates on small, indexed datasets efficiently.
User History (Join + Sort)	mean ≈ 52.11 / p95 ≈ 52.13	mean ≈ 8.33 / p95 ≈ 8.3	PostgreSQL’s relational joins outperform Mongo’s $lookup for this dataset size.
💡 Key Takeaways

For structured, moderate-size datasets, PostgreSQL’s optimizer and indexing deliver faster reads and joins.
MongoDB, while slower here, provides schema flexibility, document-oriented modeling, and horizontal scaling for dynamic or unstructured data.

In production-scale systems, both can coexist:

MongoDB for ingestion and flexible data structures.
PostgreSQL (or a warehouse) for analytical reporting.

⚖️ Summary

This project intentionally highlights the trade-off:
NoSQL offers flexibility, SQL offers raw analytical performance.
Even though the project is titled NoSQL_MovieRatings, it demonstrates that real engineering requires choosing the right tool for the workload — not ideology.

🧩 Conclusion

The NoSQL_MovieRatings project implemented a full NoSQL workflow with data ingestion, modeling, and analytics — then benchmarked it against a relational system to measure trade-offs.

Result: PostgreSQL was faster on this structured dataset, but MongoDB provides greater adaptability and scalability for evolving data structures.
Through this, we learned that:
MongoDB simplifies working with nested, evolving, and semi-structured data.
PostgreSQL remains unbeatable for heavy analytical joins on well-defined schemas.
Hybrid architectures combining MongoDB + SQL + Spark deliver both agility and analytical power.

Tech Stack:
Python · PyMongo · psycopg2 · Docker Compose · MongoDB · PostgreSQL · Pandas

Next Steps:
Add Spark–MongoDB integration.
Extend aggregations with “Top Trending Movies (30 days)” window.
Visualize benchmark results via Looker Studio or Plotly.

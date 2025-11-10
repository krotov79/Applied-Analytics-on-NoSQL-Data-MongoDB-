# 02_NoSQL_MovieRatings
MongoDB NoSQL Movie Ratings — schema, indexes, aggregations, latency benchmark; optional Spark connector

# 02_NoSQL_MovieRatings — MongoDB Implementation

**Stack:** MongoDB 7, PyMongo, Python 3.11, Docker, (baseline) PostgreSQL 16, optional Spark.

## Goals
- Design NoSQL schema + indexes
- Load & query large ratings dataset (CRUD + aggregations)
- Compare query latency & schema flexibility vs SQL
- (Optional) Spark + Mongo hybrid workflow

```flowchart LR
  A[CSV: ratings/movies/users] --> B[Loader (Python + PyMongo)]
  B --> C[(MongoDB)]
  C <--> D[Aggregations (Mongo Pipeline)]
  C <--> E[Spark (Mongo Connector) — optional]
  A --> F[(Postgres baseline — optional)]
  F <--> G[SQL Benchmarks]
  C <--> H[NoSQL Benchmarks]


## Quickstart
```bash
docker compose up -d
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python src/load_data.py

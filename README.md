# Grand Exchange Metrics
`gem` is an ETL pipeline for collecting osrs GE price data.
It periodically fetches price data from OSRS Wiki API, archives the raw data as `JSON`, transforms and loads the data to PostgreSQL for storage and analysis.

## Requirements

```
Python 3.14+
PostgreSQL 18+
```

With the following `python` packages:

```
psycopg
requests
```

## Installation

Clone the repo

```bash
git clone https://github.com/mhiillos/gem.git
cd gem
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Database setup
Create a PostgreSQL database, and set environment variable `DB_URL` for the database:

```sql
CREATE DATABASE gem;
```

```bash
export DB_URL="postgresql://<username>:<password>@localhost:5432/gem"
```

Initialize the database:

```bash
python -m scripts.init_db
```

Backfill historical data (see below):

```bash
python -m scripts.backfill
```

Fetch the latest data from OSRS Wiki:
```bash
python -m src.ingestion.fetch_latest
```

Process a single raw `JSON` snapshot and load it into the database:

```bash
python -m scripts.run_pipeline data/raw/2026-06-22/example.json
```


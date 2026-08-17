# Grand Exchange Metrics

`gem` is a small Python ETL pipeline for collecting and analyzing Old School RuneScape Grand Exchange price data.

It periodically fetches price data from the OSRS Wiki API, archives the raw JSON snapshots, transforms the data, and loads it into PostgreSQL for storage and analysis.

## Requirements

* Python 3.14+
* PostgreSQL 18+

Python packages:

```text
psycopg
requests
tabulate
pytest
matplotlib
```

## Installation

Clone the repository:

```bash
git clone https://github.com/mhiillos/gem.git
cd gem
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install:

```bash
pip install .
```

## Database setup

Create the database:

```sql
CREATE DATABASE gem;
```

Set the database connection:

```bash
export DB_URL="postgresql://<username>:<password>@localhost:5432/gem"
```

Initialize the database:

```bash
python -m scripts.init_db
```

## Pipeline

```text
OSRS Wiki API
      ↓
raw JSON snapshot
      ↓
transform
      ↓
PostgreSQL
      ↓
analysis / graphs
```

Raw snapshots are stored under:

```text
data/raw/YYYY-MM-DD/
```

This allows historical snapshots to be reprocessed later.

## Usage

Fetch the latest snapshot and update the database:

```bash
gem update
```

Backfill archived snapshots:

```bash
gem backfill
```

Force a backfill, including snapshots older than the current database watermark:

```bash
gem backfill --force
```

Run an analysis query:

```bash
gem analyze alch
```

Graph an item's high and low prices over the last 7 days:

```bash
gem graph "Abyssal whip"
```

Run tests:

```bash
pytest -q
```

## Database

GEM uses two main tables:

```text
dim_item
fact_item
```

`dim_item` stores item metadata such as name, high alchemy value, and buy limit.

`fact_item` stores historical high/low prices and their market timestamps.

Fact records use:

```text
(item_id, timestamp, type)
```

as a unique key, so reprocessing the same snapshot does not create duplicate records.

## Automation

The gem update command can be run manually or scheduled using any job scheduler.

For example, an hourly cron job could be:

```cron
0 * * * * cd /home/user/projects/gem && /home/user/projects/gem/venv/bin/gem update >> /home/user/projects/gem/logs.log 2>&1
```


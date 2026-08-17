import argparse
import os, sys
import psycopg
from gem.analysis.queries import run_query
from gem.analysis.format import print_table
from gem.ingestion.fetch_latest import fetch_latest
from gem.analysis.graph import graph
from gem.backfill import backfill

HELP = """Commands:

gem analyze <query>:   Runs an SQL query from gem/sql/
gem update:            Fetches a snapshot and updates the database with latest item data
gem graph <item_name>: Provides price data plots of item lows and highs
gem help:              Displays this help string"""

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("command", nargs="?", default="help")
  parser.add_argument("argument", nargs="*")
  parser.add_argument("--force", action="store_true")
  args = parser.parse_args()

  # Check environment variable is set to access database
  if not os.environ.get("DB_URL"):
    print("[gem] DB_URL not set")
    return 1

  try:
    match args.command:
      case "help":
        print(HELP)

      case "analyze":
        query = args.argument[0]
        try:
          rows, headers = run_query(query)
          print_table(rows, headers)
        except FileNotFoundError:
          print(f"[gem] query does not exist: {query}.sql")
          return 1

      case "update":
          fetch_latest()
          backfill()

      case "graph":
        item_name = args.argument[0]
        graph(item_name)

      case "backfill":
        backfill(args.force)

  except psycopg.ProgrammingError as e:
    print(f"[gem] database configuration/query error: {e}")
    return 1

  except psycopg.OperationalError as e:
    print(f"[gem] could not connect to database: {e}")
    return 1

  return 0

if __name__=="__main__":
  sys.exit(main())


import argparse
from gem.analysis.queries import run_query
from gem.analysis.format import print_table
from gem.ingestion.fetch_latest import fetch_latest
from gem.transform.run_pipeline import run_pipeline
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
        exit(1)

    case "update":
      fetch_latest()
      # backfill in case first to not miss any ingested data
      backfill()

    case "graph":
      item_name = args.argument[0]
      graph(item_name)

    case "backfill":
      backfill(args.force)

if __name__=="__main__":
  main()


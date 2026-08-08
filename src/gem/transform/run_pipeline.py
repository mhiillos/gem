# This scirpt takes a file path as an argument, transforms and loads the data to the database.
#
# Usage: python -m scripts.run_pipeline path/to/file.json

from gem.ingestion.ge_client import get_mapping
from gem.transform.transform import transform
from gem.db.loader import load
import argparse
import json
import sys

def run_pipeline(file_path, update_mapping=False):
  with open(file_path, "r") as f:
    data = json.load(f)
    mapping = get_mapping(update_mapping)
    dim_entries, fact_entries = transform(data, mapping)
    try:
      sys.stdout.write(f"[gem] Loading {len(dim_entries)} dim rows, {len(fact_entries)} fact rows to database...")
      load(dim_entries, fact_entries)
    except Exception as e:
      sys.stderr.write(f"[gem] error loading data to database: {e}\n")
      raise

    sys.stdout.write("ok\n")

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("file_path", type=str)
  parser.add_argument("--update_mapping", action="store_true")
  args = parser.parse_args()
  run_pipeline(args.file_path, args.update_mapping)


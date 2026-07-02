# This scirpt takes a file path as an argument, transforms and loads the data to the database.
#
# Usage: python -m scripts.run_pipeline path/to/file.json

from src.ingestion.ge_client import get_mapping
from src.transform.transform import transform
from src.db.loader import load
from pathlib import Path
import argparse
import json

def run_pipeline(file_path, update_mapping=False):
  with open(file_path, "r") as f:
    data = json.load(f)
    mapping = get_mapping(update_mapping)
    dim_entries, fact_entries = transform(data, mapping)
    load(dim_entries, fact_entries)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("file_path", type=str)
  parser.add_argument("--update_mapping", action="store_true")
  args = parser.parse_args()
  run_pipeline(args.file_path, args.update_mapping)


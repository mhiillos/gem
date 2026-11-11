# This script takes a file path as an argument, and loads one archived /1h snapshot into raw.prices_1h
#
# Usage: python -m gem.transform.run_pipeline path/to/file.json

from decimal import Decimal
from pathlib import Path
from gem.transform.transform import flatten_prices
from gem.db.loader import load_prices
import argparse
import json
import sys

def run_pipeline(file_path, source_file=None):
  if source_file is None:
    source_file = Path(file_path).name

  with open(file_path, "r") as f:
    data = json.load(f, parse_float=Decimal)
    prices = flatten_prices(data, str(source_file))
    sys.stdout.write(f"[gem] Loading {len(prices)} raw price rows to database...")
    load_prices(prices)
    sys.stdout.write("ok\n")

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("file_path", type=str)
  args = parser.parse_args()
  run_pipeline(args.file_path)

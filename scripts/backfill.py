# This script loops through all historical data located in data/raw/ and calls run_pipeline.py

from pathlib import Path
from scripts.run_pipeline import run_pipeline
from src.db.queries import latest_timestamp
from datetime import datetime, timezone

def main():
  base_path = Path(__file__).resolve().parents[1] / "data" / "raw"
  latest_ts = latest_timestamp()
  for file_path in sorted(base_path.rglob("*.json")):
    rawfile_ts = datetime.strptime(file_path.stem, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()
    if rawfile_ts <= latest_ts:
      print(f"[gem] database contains newer or equal data than {file_path.name}, skipping.")
      continue

    print(f"[gem] Processing {file_path.name}")
    run_pipeline(file_path)

if __name__ == "__main__":
  main()


# This script loops through all historical data located in data/raw/ and calls run_pipeline.py

from pathlib import Path
from scripts.run_pipeline import run_pipeline

def main():
  base_path = Path(__file__).resolve().parents[1] / "data" / "raw"
  for file_path in base_path.rglob("*.json"):
    print(f"Processing {file_path.name}")
    run_pipeline(file_path)

if __name__ == "__main__":
  main()


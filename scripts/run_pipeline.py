from src.ingestion.ge_client import get_mapping
from src.transform.transform import transform
from pathlib import Path
import json

def main():
  BASE_DIR = Path(__file__).resolve().parents[1]
  file_path = BASE_DIR / "data" / "raw" / "2026-06-22" / "2026-06-22T10:00:00Z.json"
  with open(file_path, "r") as f:
    data = json.load(f)
    mapping = get_mapping()
    a, b = transform(data, mapping)
    print("Done")
    print(len(a))
    print(len(b))

if __name__ == "__main__":
  main()

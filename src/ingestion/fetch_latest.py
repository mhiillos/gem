from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from ge_client import get_latest_prices

# Saves raw json data, and attaches the timestamp to it
def save_raw(data):
  timestamp = datetime.now(timezone.utc)
  date_path = timestamp.strftime("%Y-%m-%d")
  fname = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
  file_path = Path(f"data/raw/{date_path}/{fname}.json")
  file_path.parent.mkdir(parents=True, exist_ok=True)

  with open(file_path, "w") as f:
    json.dump(data, f)

  sys.stdout.write(f"[gem] fetched latest data at {fname}.\n")


def main():
  try:
    sys.stdout.write("[gem] fetching new data...\n")
    data = get_latest_prices()
    if not data or "data" not in data:
      raise ValueError("Invalid API rseponse")

    save_raw(data)
  except Exception as e:
    sys.stderr.write(f"[gem] error while fetching latest prices: {e}\n")


if __name__=="__main__":
  main()


from datetime import UTC, datetime, timedelta
import json
from pathlib import Path
import sys
from gem.ingestion.ge_client import get_1h

# Saves raw json data, and attaches the timestamp to it
def save_raw(data, prices_path=None):
  base_path = Path(__file__).resolve().parents[3]
  if prices_path is None:
    prices_path = base_path / "data" / "raw" / "prices_1h"
  timestamp = datetime.now(UTC)
  date_path = timestamp.strftime("%Y-%m-%d")
  fname = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
  full_path = prices_path / date_path / f"{fname}.json"
  full_path.parent.mkdir(parents=True, exist_ok=True)

  with open(full_path, "w") as f:
    json.dump(data, f)

  sys.stdout.write(f"[gem] fetched /1h data at {fname}.\n")
  return full_path

def last_completed_window():
  return int((datetime.now(UTC) - timedelta(hours=1)).replace(minute=0, second=0, microsecond=0).timestamp())

def fetch_1h(window_start=None, prices_path=None):
  try:
    if window_start is None:
      window_start = last_completed_window()
    window = datetime.fromtimestamp(window_start, UTC).strftime("%Y-%m-%dT%H:%MZ")

    sys.stdout.write(f"[gem] fetching /1h window {window}...\n")
    data = get_1h(window_start)
    if not data or "data" not in data:
      raise ValueError("Invalid API response")
    # The API returns an empty data dict (not an error) for unpublished or unavailable windows
    if not data["data"]:
      raise ValueError(f"no data for window {window}")
    if data.get("timestamp") != window_start:
      returned = datetime.fromtimestamp(data["timestamp"], UTC).strftime("%Y-%m-%dT%H:%MZ") if data.get("timestamp") else None
      raise ValueError(f"requested window {window}, got {returned}")

    path = save_raw(data, prices_path)
    return path

  except Exception as e:
    sys.stderr.write(f"[gem] error while fetching /1h prices: {e}\n")

if __name__=="__main__":
  fetch_1h()

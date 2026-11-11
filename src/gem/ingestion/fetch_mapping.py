from datetime import UTC, datetime
import json
from pathlib import Path
import sys
from gem.ingestion.ge_client import get_mapping

ITEMS_DIR = Path(__file__).resolve().parents[3] / "data" / "raw" / "items"

# The API does not return items in a stable order
def normalise(mapping):
  return sorted(mapping, key=lambda item: item["id"])

def latest_archived(items_dir):
  files = sorted(items_dir.glob("*.json"))
  return files[-1] if files else None

def fetch_mapping(items_dir=ITEMS_DIR):
  try:
    sys.stdout.write("[gem] fetching item mapping...\n")
    mapping = get_mapping()
    if not isinstance(mapping, list) or not mapping:
      raise ValueError("Invalid API response")

    latest = latest_archived(items_dir)
    if latest is not None and normalise(json.loads(latest.read_text())) == normalise(mapping):
      sys.stdout.write(f"[gem] mapping unchanged since {latest.stem}.\n")
      return latest

    fname = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    full_path = items_dir / f"{fname}.json"
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(json.dumps(mapping))

    sys.stdout.write(f"[gem] archived new mapping at {fname}.\n")
    return full_path

  except Exception as e:
    sys.stderr.write(f"[gem] error while fetching mapping, keeping last archived mapping: {e}\n")

if __name__ == "__main__":
  fetch_mapping()

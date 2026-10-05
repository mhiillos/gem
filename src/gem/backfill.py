# Replays the raw archive into the database: loads the newest archived mapping
# from data/raw/items/ into raw.items, then each new price file in
# data/raw/prices_1h/ into raw.prices_1h.

import json
from pathlib import Path
from gem.db.loader import load_items
from gem.db.queries import latest_price_source
from gem.ingestion.fetch_mapping import latest_archived
from gem.transform.run_pipeline import run_pipeline
from gem.transform.transform import flatten_items

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

def backfill(force=False, raw_path=None):
  if raw_path is None:
    raw_path = RAW_DIR
  prices_path = raw_path / "prices_1h"
  items_path = raw_path / "items"

  latest = latest_archived(items_path)
  if latest is None:
    print(f"[gem] No archived mapping in {items_path}, skipping items")
  else:
    with open(latest, "r") as f:
      mapping = json.load(f)
    items = flatten_items(mapping, latest.name)
    print(f"[gem] Loading {len(items)} item rows from {latest.name}")
    load_items(items)

  # Watermark is the newest loaded file; ISO-named paths sort chronologically
  latest_source = latest_price_source()
  for file_path in sorted(prices_path.rglob("*.json")):
    source_file = str(file_path.relative_to(prices_path))
    if not force and latest_source is not None and source_file <= latest_source:
      continue

    print(f"[gem] Processing {file_path.name}")
    run_pipeline(file_path, source_file)

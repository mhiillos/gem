import json
import gem.backfill
from gem.backfill import backfill
from gem.db.loader import load_prices
from gem.db.queries import latest_timestamp
from data import DATA1, DATA5, MAPPING, MAPPING2, PRICES, PRICES3, WINDOW_TS_LATER, WINDOW_DT, WINDOW_DT_LATER

def archive_paths(tmp_path):
  return tmp_path / "prices_1h", tmp_path / "items"

def write_raw_file(prices_path, timestamp, data):
  directory = prices_path / timestamp.strftime("%Y-%m-%d")
  directory.mkdir(parents=True, exist_ok=True)

  file_path = directory / (
    timestamp.strftime("%Y-%m-%dT%H:%M:%SZ") + ".json"
  )

  file_path.write_text(json.dumps(data))

  return file_path

def write_mapping_file(items_path, timestamp, data):
  items_path.mkdir(parents=True, exist_ok=True)

  file_path = items_path / (timestamp.strftime("%Y-%m-%dT%H:%M:%SZ") + ".json")
  file_path.write_text(json.dumps(data))
  return file_path

def spy_run_pipeline(monkeypatch):
  processed = []
  real_run_pipeline = gem.backfill.run_pipeline

  def spy(file_path, source_file=None):
    processed.append(str(source_file))
    real_run_pipeline(file_path, source_file)

  monkeypatch.setattr(gem.backfill, "run_pipeline", spy)
  return processed

def test_backfill_processes_new_raw_file(test_db, tmp_path):
  prices_path, items_path = archive_paths(tmp_path)
  load_prices(PRICES)

  write_raw_file(
    prices_path,
    WINDOW_DT_LATER,
    DATA5,
  )

  backfill(raw_path=tmp_path)
  assert latest_timestamp() == WINDOW_TS_LATER

  with test_db.cursor() as cur:
    cur.execute("SELECT DISTINCT _source_file FROM raw.prices_1h WHERE window_timestamp = %s", (WINDOW_DT_LATER,))
    assert cur.fetchall() == [("2026-01-01/2026-01-01T01:00:00Z.json",)]

def test_backfill_skips_already_loaded_file(test_db, tmp_path, monkeypatch):
  prices_path, items_path = archive_paths(tmp_path)
  # PRICES set the watermark to 2026-01-01/2026-01-01T00:05:00Z.json, later than this file
  load_prices(PRICES)
  processed = spy_run_pipeline(monkeypatch)

  write_raw_file(
    prices_path,
    WINDOW_DT,
    DATA1,
  )

  backfill(raw_path=tmp_path)
  assert processed == []

def test_backfill_force_processes_file(test_db, tmp_path):
  prices_path, items_path = archive_paths(tmp_path)
  load_prices(PRICES3)

  # Earlier raw file
  write_raw_file(
    prices_path,
    WINDOW_DT,
    DATA1,
  )

  # Force adding earlier datapoint
  backfill(force=True, raw_path=tmp_path)

  with test_db.cursor() as cur:
    cur.execute("""
      SELECT item_id, avg_high_price, window_timestamp
      FROM raw.prices_1h
      ORDER BY window_timestamp
    """)
    rows = cur.fetchall()
  assert ((1, 10000, WINDOW_DT) in rows)
  assert ((1, 11000, WINDOW_DT_LATER) in rows)

def test_backfill_loads_newest_mapping(test_db, tmp_path):
  prices_path, items_path = archive_paths(tmp_path)
  write_mapping_file(items_path, WINDOW_DT_LATER, MAPPING2)
  write_mapping_file(items_path, WINDOW_DT, MAPPING)
  backfill(raw_path=tmp_path)

  with test_db.cursor() as cur:
    cur.execute("""
      SELECT id, _source_file
      FROM raw.items
      ORDER BY id
    """)
    rows = cur.fetchall()
  assert rows == [(3, WINDOW_DT_LATER.strftime("%Y-%m-%dT%H:%M:%SZ") + ".json")]

def test_backfill_empty_items_path(test_db, tmp_path):
  prices_path, _ = archive_paths(tmp_path)
  write_raw_file(prices_path, WINDOW_DT, DATA1)
  backfill(raw_path=tmp_path)

  with test_db.cursor() as cur:
    cur.execute("""
      SELECT item_id
      FROM raw.prices_1h
      ORDER BY item_id
    """)
    rows = cur.fetchall()
    assert(rows == [(1,), (2,)])

def test_backfill_second_run_processes_nothing(test_db, tmp_path, monkeypatch):
  prices_path, _ = archive_paths(tmp_path)
  write_raw_file(prices_path, WINDOW_DT, DATA1)
  processed = spy_run_pipeline(monkeypatch)
  backfill(raw_path=tmp_path)
  backfill(raw_path=tmp_path)
  assert processed == ["2026-01-01/" + WINDOW_DT.strftime("%Y-%m-%dT%H:%M:%SZ") + ".json"]

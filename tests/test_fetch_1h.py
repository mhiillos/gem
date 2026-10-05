import json
from datetime import datetime, timedelta, UTC
import gem.ingestion.fetch_1h
from gem.ingestion.fetch_1h import fetch_1h, last_completed_window
from data import DATA1, WINDOW_TS

def fake_api(monkeypatch, response):
  requested = []
  def get_1h(timestamp=None):
    requested.append(timestamp)
    return response
  monkeypatch.setattr(gem.ingestion.fetch_1h, "get_1h", get_1h)
  return requested

def archived_files(prices_path):
  return list(prices_path.rglob("*.json"))

def test_fetch_1h_archives_requested_window(tmp_path, monkeypatch):
  requested = fake_api(monkeypatch, DATA1)

  path = fetch_1h(WINDOW_TS, prices_path=tmp_path)

  assert requested == [WINDOW_TS]
  assert archived_files(tmp_path) == [path]
  assert json.loads(path.read_text()) == DATA1

def test_fetch_1h_empty_data_not_archived(tmp_path, monkeypatch):
  fake_api(monkeypatch, {"timestamp": WINDOW_TS, "data": {}})

  assert fetch_1h(WINDOW_TS, prices_path=tmp_path) is None
  assert archived_files(tmp_path) == []

def test_fetch_1h_wrong_window_not_archived(tmp_path, monkeypatch):
  fake_api(monkeypatch, {**DATA1, "timestamp": WINDOW_TS - 3600})

  assert fetch_1h(WINDOW_TS, prices_path=tmp_path) is None
  assert archived_files(tmp_path) == []

def test_fetch_1h_api_error(tmp_path, monkeypatch):
  def broken_api(timestamp=None):
    raise ConnectionError("API down")
  monkeypatch.setattr(gem.ingestion.fetch_1h, "get_1h", broken_api)

  assert fetch_1h(WINDOW_TS, prices_path=tmp_path) is None
  assert archived_files(tmp_path) == []

def test_fetch_1h_defaults_to_last_completed_window(tmp_path, monkeypatch):
  window = last_completed_window()
  requested = fake_api(monkeypatch, {**DATA1, "timestamp": window})

  fetch_1h(prices_path=tmp_path)

  assert requested == [window]

def test_last_completed_window():
  window = last_completed_window()
  hour_start = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)

  # The API rejects float timestamps
  assert isinstance(window, int)
  assert window % 3600 == 0
  assert window == int((hour_start - timedelta(hours=1)).timestamp())

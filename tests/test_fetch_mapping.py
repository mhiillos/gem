import json
import gem.ingestion.fetch_mapping
from gem.ingestion.fetch_mapping import fetch_mapping
from data import MAPPING, MAPPING2

def fake_api(monkeypatch, response):
  monkeypatch.setattr(gem.ingestion.fetch_mapping, "get_mapping", lambda: response)

def test_fetch_mapping_archives_first_mapping(tmp_path, monkeypatch):
  fake_api(monkeypatch, MAPPING)

  path = fetch_mapping(items_dir=tmp_path)

  assert list(tmp_path.glob("*.json")) == [path]
  assert json.loads(path.read_text()) == MAPPING

def test_fetch_mapping_skips_reordered_mapping(tmp_path, monkeypatch):
  # Older name, so a wrongly detected change adds a second file instead of overwriting
  archived = tmp_path / "2026-01-01T00:00:00Z.json"
  archived.write_text(json.dumps(MAPPING))

  fake_api(monkeypatch, list(reversed(MAPPING)))
  path = fetch_mapping(items_dir=tmp_path)

  assert path == archived
  assert list(tmp_path.glob("*.json")) == [archived]

def test_fetch_mapping_archives_changed_mapping(tmp_path, monkeypatch):
  (tmp_path / "2026-01-01T00:00:00Z.json").write_text(json.dumps(MAPPING))

  fake_api(monkeypatch, MAPPING2)
  path = fetch_mapping(items_dir=tmp_path)

  assert len(list(tmp_path.glob("*.json"))) == 2
  assert json.loads(path.read_text()) == MAPPING2

def test_fetch_mapping_api_error(tmp_path, monkeypatch):
  def broken_api():
    raise ConnectionError("API down")
  monkeypatch.setattr(gem.ingestion.fetch_mapping, "get_mapping", broken_api)

  assert fetch_mapping(items_dir=tmp_path) is None
  assert list(tmp_path.glob("*.json")) == []

def test_fetch_mapping_empty_response(tmp_path, monkeypatch):
  fake_api(monkeypatch, [])

  assert fetch_mapping(items_dir=tmp_path) is None
  assert list(tmp_path.glob("*.json")) == []

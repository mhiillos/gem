from datetime import datetime, UTC
import math
import gem.analysis.graph
from gem.analysis.graph import graph

T0 = datetime(2026, 11, 1, 0, tzinfo=UTC)
T1 = datetime(2026, 11, 1, 1, tzinfo=UTC)

# Second row is no trades
ROWS = [
  (T0, 120, 100, 5, 7),
  (T1, None, None, None, None),
]

def fake_graph_deps(monkeypatch, rows):
  calls = []
  monkeypatch.setattr(gem.analysis.graph, "run_query", lambda query, params: (rows, None))
  monkeypatch.setattr(gem.analysis.graph, "plot", lambda *args: calls.append(args))
  return calls

def test_graph_passes_query_rows_to_plot(monkeypatch):
  calls = fake_graph_deps(monkeypatch, ROWS)

  graph("test item")

  assert len(calls) == 1
  item_name, _, high_prices, low_prices, high_volume, low_volume = calls[0]
  assert item_name == "test item"
  assert high_prices[0] == 120
  assert low_prices[0] == 100
  assert high_volume[0] == 5
  assert low_volume[0] == 7
  assert math.isnan(high_volume[1])

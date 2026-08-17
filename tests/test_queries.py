from gem.db.loader import load
from gem.analysis.queries import run_query
from data import DIMS2, FACTS2

# Tests currently rely on current time, if the hour changes between setup and the query, it will fail. However unlikely to happen.

def test_run_query_no_parameter(test_db):
  load(DIMS2, FACTS2)
  res, _ = run_query("alch")
  expected_res = [("test1", 11000, 5000, 32, 6000, 120.0)]
  assert res == expected_res

def test_item_graph_7d_has_169_datapoints(test_db):
  load(DIMS2, FACTS2)
  res, _ = run_query("item_graph_7d", ("test1",))
  assert  len(res) == 169

def test_item_graph_7d_data_at_correct_spot(test_db):
  load(DIMS2, FACTS2)
  res, _ = run_query("item_graph_7d", ("test1",))
  highs = [x[1] for x in res]
  lows = [x[2] for x in res]
  assert highs[-2] == 10000
  assert not lows[-2]

  assert lows[-3] == 5000
  assert not highs[-3]


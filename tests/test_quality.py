from gem.db.loader import load
from data import DIMS, FACTS2, FACTS7
from gem.db.queries import latest_timestamp
from datetime import datetime, timedelta

# Freshness defined as latest data being at most 1 hour old.
def test_freshness_true(test_db):
  load(DIMS, FACTS7)
  latest_ts = latest_timestamp()
  diff = datetime.now() - datetime.fromtimestamp(latest_timestamp())
  assert diff < timedelta(hours=1)

def test_freshness_false(test_db):
  load(DIMS, FACTS2)
  latest_ts = latest_timestamp()
  diff = datetime.now() - datetime.fromtimestamp(latest_timestamp())
  assert diff > timedelta(hours=1)


from gem.transform.transform import transform
from data import DATA1, DATA2, DATA3, DATA4, MAPPING, DIMS, FACTS, FACTS5, FACTS6, WINDOW_DT, WINDOW_TS


def test_transform_valid_data():
  dim, fact = transform(DATA1, MAPPING)
  assert dim == DIMS
  assert fact == FACTS

def test_transform_missing_high_price():
  _, fact = transform(DATA2, MAPPING)
  assert fact == FACTS5

def test_transform_missing_low_price():
  _, fact = transform(DATA3, MAPPING)
  assert fact == FACTS6

def test_transform_unknown_item():
  _, fact = transform(DATA4, MAPPING)
  assert fact == [{
    "item_id": 3, "high_price": 10000, "low_price": 5000,
    "high_price_volume": 50, "low_price_volume": 30,
    "window_timestamp": WINDOW_DT,
  }]

def test_empty_data():
  _, fact = transform({"timestamp": WINDOW_TS, "data": {}}, MAPPING)
  assert fact == []


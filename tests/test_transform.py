from gem.transform.transform import transform
from data import DATA1, DATA2, DATA3, DATA4, MAPPING, DIMS, FACTS, FACTS5, FACTS6


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
  assert fact == []

def test_empty_data():
  _, fact = transform({"data": {}}, MAPPING)
  assert fact == []


import unittest
from datetime import datetime, UTC
from src.transform.transform import transform

# Clean data
DATA_1 = {
  "data": {
    "1": {
      "high": 10000,
      "highTime": 1767225600,
      "low": 5000,
      "lowTime": 1767225500
    },
    "2": {
      "high": 20000,
      "highTime": 1767225600,
      "low": 10000,
      "lowTime": 1767225500
    }
  }
}

# Data with missing high price
DATA_2 = {
  "data": {
    "1": {
      "high": None,
      "highTime": None,
      "low": 5000,
      "lowTime": 1767225500
    }
  }
}

# Data with missing low price
DATA_3 = {
  "data": {
    "1": {
      "high": 10000,
      "highTime": 1767225500,
      "low": None,
      "lowTime": None
    }
  }
}

# Data with an item that does not exist in mapping
DATA_4 = {
  "data": {
    "3": {
      "high": 10000,
      "highTime": 1767225500,
      "low": 5000,
      "lowTime": 1767225500
    }
  }
}

MAPPING = [
  {
    "examine": "test1",
    "id": 1,
    "members": True,
    "lowalch": 60000,
    "limit": 8,
    "value": 150000,
    "highalch": 90000,
    "icon": "test1.png",
    "name": "test1"
  },
  {
    "examine": "test2",
    "id": 2,
    "members": True,
    "lowalch": 60000,
    "limit": 4,
    "value": 150000,
    "highalch": 1,
    "icon": "test2.png",
    "name": "test2"
  }
]

DIM_1 = [
  {
    "item_id": 1,
    "name": "test1",
    "high_alch": 90000,
    "buy_limit": 8
  },
  {
    "item_id": 2,
    "name": "test2",
    "high_alch": 1,
    "buy_limit": 4
  }
]

FACT_1 = [
  {
  "item_id": 1,
  "price": 10000,
  "timestamp": datetime.fromtimestamp(1767225600, UTC),
  "type": "high"
  },
  {
  "item_id": 1,
  "price": 5000,
  "timestamp": datetime.fromtimestamp(1767225500, UTC),
  "type": "low"
  },
  {
  "item_id": 2,
  "price": 20000,
  "timestamp": datetime.fromtimestamp(1767225600, UTC),
  "type": "high"
  },
  {
  "item_id": 2,
  "price": 10000,
  "timestamp": datetime.fromtimestamp(1767225500, UTC),
  "type": "low"
  }
]

FACT_2 = [
  {
  "item_id": 1,
  "price": 5000,
  "timestamp": datetime.fromtimestamp(1767225500, UTC),
  "type": "low"
  }
]

FACT_3 = [
  {
  "item_id": 1,
  "price": 10000,
  "timestamp": datetime.fromtimestamp(1767225500, UTC),
  "type": "high"
  }
]

class TestTransform(unittest.TestCase):

  def test_transform_valid_data(self):
    dim, fact = transform(DATA_1, MAPPING)
    self.assertEqual(dim, DIM_1)
    self.assertEqual(fact, FACT_1)

  def test_transform_missing_high_price(self):
    _, fact = transform(DATA_2, MAPPING)
    self.assertEqual(fact, FACT_2)

  def test_transform_missing_low_price(self):
    _, fact = transform(DATA_3, MAPPING)
    self.assertEqual(fact, FACT_3)

  def test_transform_unknown_item(self):
    _, fact = transform(DATA_4, MAPPING)
    self.assertEqual(fact, [])

  def test_empty_data(self):
    _, fact = transform({"data": {}}, MAPPING)
    self.assertEqual(fact, [])

if __name__ == "__main__":
  unittest.main()


from datetime import datetime, timedelta, UTC

# Clean data
DATA1 = {
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
DATA2 = {
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
DATA3 = {
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
DATA4 = {
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


DIMS = [
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

DIMS2 = [
  {
    "item_id": 1,
    "name": "test1",
    "high_alch": 11000,
    "buy_limit": 32
  },
  {
    "item_id": 2,
    "name": "test2",
    "high_alch": 1,
    "buy_limit": 8
  }
]

FACTS = [
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

FACTS2 = [
  {
  "item_id": 1,
  "price": 10000,
  "timestamp": datetime.now(UTC) - timedelta(hours=1),
  "type": "high"
  },
  {
  "item_id": 1,
  "price": 5000,
  "timestamp": datetime.now(UTC) - timedelta(hours=2),
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

FACTS3 = [{
  "item_id": 1,
  "price": 11000,
  "timestamp": datetime.fromtimestamp(1767225700, UTC),
  "type": "high"
}]

FACTS4 = [{
  "item_id": 5,
  "price": 10000,
  "timestamp": datetime.now(UTC),
  "type": "high"
}]

FACTS5 = [{
  "item_id": 1,
  "price": 5000,
  "timestamp": datetime.fromtimestamp(1767225500, UTC),
  "type": "low"
}]

FACTS6 = [{
  "item_id": 1,
  "price": 10000,
  "timestamp": datetime.fromtimestamp(1767225500, UTC),
  "type": "high"
}]

FACTS7 = [{
  "item_id": 1,
  "price": 10000,
  "timestamp": datetime.now(),
  "type": "high"
  }]

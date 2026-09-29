from datetime import datetime, timedelta, UTC

WINDOW_TS = 1767225600
WINDOW_TS_LATER = WINDOW_TS + 3600
WINDOW_DT = datetime.fromtimestamp(WINDOW_TS, UTC)
WINDOW_DT_LATER = datetime.fromtimestamp(WINDOW_TS_LATER, UTC)

# Clean data
DATA1 = {
  "timestamp": WINDOW_TS,
  "data": {
    "1": {
      "avgHighPrice": 10000,
      "highPriceVolume": 50,
      "avgLowPrice": 5000,
      "lowPriceVolume": 30
    },
    "2": {
      "avgHighPrice": 20000,
      "highPriceVolume": 20,
      "avgLowPrice": 10000,
      "lowPriceVolume": 15
    },
  }
}

# Data with missing high price
DATA2 = {
  "timestamp": WINDOW_TS,
  "data": {
    "1": {
      "avgHighPrice": None,
      "highPriceVolume": 0,
      "avgLowPrice": 5000,
      "lowPriceVolume": 30
    }
  }
}

# Data with missing low price
DATA3 = {
  "timestamp": WINDOW_TS,
  "data": {
    "1": {
      "avgHighPrice": 10000,
      "highPriceVolume": 50,
      "avgLowPrice": None,
      "lowPriceVolume": 0
    }
  }
}

# Data with an item that does not exist in mapping
DATA4 = {
  "timestamp": WINDOW_TS,
  "data": {
    "3": {
      "avgHighPrice": 10000,
      "highPriceVolume": 50,
      "avgLowPrice": 5000,
      "lowPriceVolume": 30
    }
  }
}

DATA5 = {
  "timestamp": WINDOW_TS_LATER,
  "data": {
    "1": {
      "avgHighPrice": 11000,
      "highPriceVolume": 40,
      "avgLowPrice": None,
      "lowPriceVolume": 0
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
    "high_price": 10000,
    "low_price": 5000,
    "high_price_volume": 50,
    "low_price_volume": 30,
    "window_timestamp": WINDOW_DT
  },
  {
    "item_id": 2,
    "high_price": 20000,
    "low_price": 10000,
    "high_price_volume": 20,
    "low_price_volume": 15,
    "window_timestamp": WINDOW_DT
  }
]

FACTS2 = [
  {
    "item_id": 1,
    "high_price": 10000,
    "low_price": None,
    "high_price_volume": 50,
    "low_price_volume": 0,
    "window_timestamp": datetime.now(UTC).replace(
      minute=0, second=0, microsecond=0
    ) - timedelta(hours=1)
  },
  {
    "item_id": 1,
    "high_price": None,
    "low_price": 5000,
    "high_price_volume": 0,
    "low_price_volume": 30,
    "window_timestamp": datetime.now(UTC).replace(
      minute=0, second=0, microsecond=0
    ) - timedelta(hours=2)
  },
  {
    "item_id": 2,
    "high_price": 20000,
    "low_price": 10000,
    "high_price_volume": 20,
    "low_price_volume": 15,
    "window_timestamp": WINDOW_DT
  }
]

FACTS3 = [{
  "item_id": 1,
  "high_price": 11000,
  "low_price": None,
  "high_price_volume": 40,
  "low_price_volume": 0,
  "window_timestamp": WINDOW_DT_LATER
}]

FACTS4 = [{
  "item_id": 5,
  "high_price": 10000,
  "low_price": None,
  "high_price_volume": 12,
  "low_price_volume": 0,
  "window_timestamp": datetime.now(UTC)
}]

FACTS5 = [{
  "item_id": 1,
  "high_price": None,
  "low_price": 5000,
  "high_price_volume": 0,
  "low_price_volume": 30,
  "window_timestamp": WINDOW_DT
}]

FACTS6 = [{
  "item_id": 1,
  "high_price": 10000,
  "low_price": None,
  "high_price_volume": 50,
  "low_price_volume": 0,
  "window_timestamp": WINDOW_DT
}]

FACTS7 = [{
  "item_id": 1,
  "high_price": 10000,
  "low_price": None,
  "high_price_volume": 50,
  "low_price_volume": 0,
  "window_timestamp": datetime.now(UTC)
}]

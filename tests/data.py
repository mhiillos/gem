from datetime import datetime, timedelta, UTC
from decimal import Decimal

WINDOW_TS = 1767225600
WINDOW_TS_LATER = WINDOW_TS + 3600
WINDOW_DT = datetime.fromtimestamp(WINDOW_TS, UTC)
WINDOW_DT_LATER = datetime.fromtimestamp(WINDOW_TS_LATER, UTC)

SOURCE_FILE = "2026-01-01/2026-01-01T00:05:00Z.json"
SOURCE_FILE_LATER = "2026-01-01/2026-01-01T01:05:00Z.json"
MAPPING_SOURCE_FILE = "mapping/2026-01-01T00:05:00Z.json"

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

# Fractional price (as parsed with parse_float=Decimal) and a missing volume key
DATA6 = {
  "timestamp": WINDOW_TS,
  "data": {
    "1": {
      "avgHighPrice": Decimal("12.37"),
      "highPriceVolume": 5,
      "avgLowPrice": None
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

# Item without the optional limit/lowalch/highalch fields
MAPPING2 = [
  {
    "examine": "test3",
    "id": 3,
    "members": False,
    "value": 10,
    "icon": "test3.png",
    "name": "test3"
  }
]

ITEMS = [
  {
    "id": 1,
    "examine": "test1",
    "members": True,
    "lowalch": 60000,
    "buy_limit": 8,
    "value": 150000,
    "highalch": 90000,
    "icon": "test1.png",
    "name": "test1",
    "_source_file": MAPPING_SOURCE_FILE
  },
  {
    "id": 2,
    "examine": "test2",
    "members": True,
    "lowalch": 60000,
    "buy_limit": 4,
    "value": 150000,
    "highalch": 1,
    "icon": "test2.png",
    "name": "test2",
    "_source_file": MAPPING_SOURCE_FILE
  }
]

# Same items after a game update changed alch values and buy limits
ITEMS2 = [
  {
    "id": 1,
    "examine": "test1",
    "members": True,
    "lowalch": 60000,
    "buy_limit": 32,
    "value": 150000,
    "highalch": 11000,
    "icon": "test1.png",
    "name": "test1",
    "_source_file": MAPPING_SOURCE_FILE
  },
  {
    "id": 2,
    "examine": "test2",
    "members": True,
    "lowalch": 60000,
    "buy_limit": 8,
    "value": 150000,
    "highalch": 1,
    "icon": "test2.png",
    "name": "test2",
    "_source_file": MAPPING_SOURCE_FILE
  }
]

# Expected flatten_items(MAPPING2): missing optional fields become None
ITEMS3 = [
  {
    "id": 3,
    "examine": "test3",
    "members": False,
    "lowalch": None,
    "buy_limit": None,
    "value": 10,
    "highalch": None,
    "icon": "test3.png",
    "name": "test3",
    "_source_file": MAPPING_SOURCE_FILE
  }
]

# Expected flatten_prices(DATA1)
PRICES = [
  {
    "item_id": 1,
    "window_timestamp": WINDOW_DT,
    "avg_high_price": 10000,
    "high_price_volume": 50,
    "avg_low_price": 5000,
    "low_price_volume": 30,
    "_source_file": SOURCE_FILE
  },
  {
    "item_id": 2,
    "window_timestamp": WINDOW_DT,
    "avg_high_price": 20000,
    "high_price_volume": 20,
    "avg_low_price": 10000,
    "low_price_volume": 15,
    "_source_file": SOURCE_FILE
  }
]

PRICES2 = [
  {
    "item_id": 1,
    "window_timestamp": datetime.now(UTC).replace(
      minute=0, second=0, microsecond=0
    ) - timedelta(hours=1),
    "avg_high_price": 10000,
    "high_price_volume": 50,
    "avg_low_price": None,
    "low_price_volume": 0,
    "_source_file": SOURCE_FILE
  },
  {
    "item_id": 1,
    "window_timestamp": datetime.now(UTC).replace(
      minute=0, second=0, microsecond=0
    ) - timedelta(hours=2),
    "avg_high_price": None,
    "high_price_volume": 0,
    "avg_low_price": 5000,
    "low_price_volume": 30,
    "_source_file": SOURCE_FILE
  },
  {
    "item_id": 2,
    "window_timestamp": WINDOW_DT,
    "avg_high_price": 20000,
    "high_price_volume": 20,
    "avg_low_price": 10000,
    "low_price_volume": 15,
    "_source_file": SOURCE_FILE
  }
]

# Expected flatten_prices(DATA5)
PRICES3 = [{
  "item_id": 1,
  "window_timestamp": WINDOW_DT_LATER,
  "avg_high_price": 11000,
  "high_price_volume": 40,
  "avg_low_price": None,
  "low_price_volume": 0,
  "_source_file": SOURCE_FILE_LATER
}]

# Item that is not in raw.items: raw has no FK, so this must load
PRICES4 = [{
  "item_id": 5,
  "window_timestamp": WINDOW_DT,
  "avg_high_price": 10000,
  "high_price_volume": 12,
  "avg_low_price": None,
  "low_price_volume": 0,
  "_source_file": SOURCE_FILE
}]

# Expected flatten_prices(DATA2)
PRICES5 = [{
  "item_id": 1,
  "window_timestamp": WINDOW_DT,
  "avg_high_price": None,
  "high_price_volume": 0,
  "avg_low_price": 5000,
  "low_price_volume": 30,
  "_source_file": SOURCE_FILE
}]

# Expected flatten_prices(DATA3)
PRICES6 = [{
  "item_id": 1,
  "window_timestamp": WINDOW_DT,
  "avg_high_price": 10000,
  "high_price_volume": 50,
  "avg_low_price": None,
  "low_price_volume": 0,
  "_source_file": SOURCE_FILE
}]

# Expected flatten_prices(DATA6): Decimal kept exact, missing volume stays None
PRICES7 = [{
  "item_id": 1,
  "window_timestamp": WINDOW_DT,
  "avg_high_price": Decimal("12.37"),
  "high_price_volume": 5,
  "avg_low_price": None,
  "low_price_volume": None,
  "_source_file": SOURCE_FILE
}]

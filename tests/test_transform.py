from gem.transform.transform import flatten_prices, flatten_items
from data import DATA1, DATA2, DATA3, DATA4, DATA6, MAPPING, MAPPING2, ITEMS, ITEMS3, PRICES, PRICES5, PRICES6, PRICES7, SOURCE_FILE, MAPPING_SOURCE_FILE, WINDOW_DT, WINDOW_TS


def test_flatten_prices_valid_data():
  assert flatten_prices(DATA1, SOURCE_FILE) == PRICES

def test_flatten_prices_missing_high_price():
  assert flatten_prices(DATA2, SOURCE_FILE) == PRICES5

def test_flatten_prices_missing_low_price():
  assert flatten_prices(DATA3, SOURCE_FILE) == PRICES6

def test_flatten_prices_keeps_decimals_and_missing_keys():
  assert flatten_prices(DATA6, SOURCE_FILE) == PRICES7

def test_flatten_prices_unknown_item():
  assert flatten_prices(DATA4, SOURCE_FILE) == [{
    "item_id": 3, "window_timestamp": WINDOW_DT,
    "avg_high_price": 10000, "high_price_volume": 50,
    "avg_low_price": 5000, "low_price_volume": 30,
    "_source_file": SOURCE_FILE,
  }]

def test_flatten_prices_empty_data():
  assert flatten_prices({"timestamp": WINDOW_TS, "data": {}}, SOURCE_FILE) == []

def test_flatten_items_valid_data():
  assert flatten_items(MAPPING, MAPPING_SOURCE_FILE) == ITEMS

def test_flatten_items_missing_optional_fields():
  assert flatten_items(MAPPING2, MAPPING_SOURCE_FILE) == ITEMS3

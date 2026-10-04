from datetime import datetime, UTC
from decimal import Decimal
from typing import TypedDict

class PriceRow(TypedDict):
  item_id: int
  window_timestamp: datetime
  avg_high_price: Decimal | None
  high_price_volume: int | None
  avg_low_price: Decimal | None
  low_price_volume: int | None
  _source_file: str

class ItemRow(TypedDict):
  id: int
  examine: str
  members: bool
  lowalch: int
  buy_limit: int
  value: int
  highalch: int
  icon: str
  name: str
  _source_file: str

def flatten_prices(data, source_file):
  prices: list[PriceRow] = []
  window_timestamp = datetime.fromtimestamp(data["timestamp"], UTC)
  for k, v in data["data"].items():
    prices.append({
      "item_id": int(k),
      "window_timestamp": window_timestamp,
      "avg_high_price": v.get("avgHighPrice"),
      "high_price_volume": v.get("highPriceVolume"),
      "avg_low_price": v.get("avgLowPrice"),
      "low_price_volume": v.get("lowPriceVolume"),
      "_source_file": source_file
    })
  return prices

def flatten_items(data, source_file):
  items: list[ItemRow] = []
  for item in data:
    items.append({
      "id": item["id"],
      "examine": item.get("examine"),
      "members": item.get("members"),
      "lowalch": item.get("lowalch"),
      "buy_limit": item.get("limit"),
      "value": item.get("value"),
      "highalch": item.get("highalch"),
      "icon": item.get("icon"),
      "name": item.get("name"),
      "_source_file": source_file
    })
  return items


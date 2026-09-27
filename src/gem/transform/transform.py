from datetime import datetime, UTC
from typing import TypedDict

class DimItem(TypedDict):
  item_id: int
  name: str
  high_alch: int
  buy_limit: int


class FactItem(TypedDict):
  item_id: int
  high_price: int | None
  low_price: int | None
  high_price_volume: int
  low_price_volume: int
  window_timestamp: datetime

def parse_price(v, key):
  val = v.get(key)
  return int(val) if val is not None else None

# Transform input JSON object into dimension table and fact table entries
def transform(data, mapping):
  dim_entries: list[DimItem] = []
  fact_entries: list[FactItem] = []

  for item in mapping:
    dim_entries.append({
      "item_id": int(item["id"]),
      "name": item["name"],
      "high_alch": int(item.get("highalch", 0)),
      "buy_limit": int(item.get("limit", 0))
    })

  window_timestamp = datetime.fromtimestamp(data["timestamp"], UTC)
  for k, v in data["data"].items():
    fact_entries.append({
      "item_id": int(k),
      "high_price": parse_price(v, "avgHighPrice"),
      "low_price": parse_price(v, "avgLowPrice"),
      "high_price_volume": int(v.get("highPriceVolume", 0)),
      "low_price_volume": int(v.get("lowPriceVolume", 0)),
      "window_timestamp": window_timestamp,
    })

  return (dim_entries, fact_entries)


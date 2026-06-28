from typing import TypedDict, Literal
import json

class DimItem(TypedDict):
  item_id: int
  name: str
  high_alch: int
  buy_limit: int

ItemType = Literal["high", "low"]

class FactItem(TypedDict):
  item_id: int
  price: int
  timestamp: int
  type: ItemType

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

  for k, v in data["data"].items():
    # Add high and low data separately
    if v.get("high") is not None:
      fact_entries.append({
        "item_id": int(k),
        "price": int(v.get("high", 0)),
        "timestamp": v["highTime"],
        "type": "high"
      })
    if v.get("low") is not None:
      fact_entries.append({
        "item_id": int(k),
        "price": int(v.get("low", 0)),
        "timestamp": v["lowTime"],
        "type": "low"
      })

  return (dim_entries, fact_entries)


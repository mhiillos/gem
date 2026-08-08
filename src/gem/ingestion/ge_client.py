import requests
import json
import sys
from pathlib import Path

BASE_URL = "https://prices.runescape.wiki/api/v1/osrs"

HEADERS = {
    "User-Agent": "gem - github.com/mhiillos/gem"
    }

MAPPING_CACHE = Path(__file__).parents[2] / "data" / "cache" / "mapping.json"

# Fetches the latest price information for every item, or for a single item given by ID.
def get_latest_prices(id = None):
  url = f"{BASE_URL}/latest"
  params = {
    "id": id
  }
  response = requests.get(url, headers=HEADERS, params=params)
  response.raise_for_status()
  return response.json()

# Fetches list of objects mapping the ID with name and other information.
def get_mapping(update_mapping=False):
  url = f"{BASE_URL}/mapping"
  if not MAPPING_CACHE.exists() or update_mapping:
    sys.stdout.write("[gem] fetching new mapping from api...")
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    MAPPING_CACHE.parent.mkdir(parents=True, exist_ok=True)
    MAPPING_CACHE.write_text(json.dumps(response.json()))
    sys.stdout.write("ok\n")
    return response.json()
  else:
    return json.loads(MAPPING_CACHE.read_text())

# Fetches the timeseries data of the given item by id and time-interval
def get_timeseries(id, timestep):
  url = f"{BASE_URL}/timeseries"
  params = {
      "id": id,
      "timestep": timestep
      }
  response = requests.get(url, headers=HEADERS, params=params)
  response.raise_for_status()
  return response.json()


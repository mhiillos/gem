import requests

BASE_URL = "https://prices.runescape.wiki/api/v1/osrs"

HEADERS = {
    "User-Agent": "gem - github.com/mhiillos/gem"
    }

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
def get_mapping():
  url = f"{BASE_URL}/mapping"
  response = requests.get(url, headers=HEADERS)
  response.raise_for_status()
  return response.json()

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


from gem.db.connection import get_connection

def latest_timestamp():
  query = """
  SELECT MAX(window_timestamp)
  FROM raw.prices_1h
  """
  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(query)
      response = cur.fetchone()[0]

      if response is None:
        return 0

      return response.timestamp()

def latest_price_source():
  query = """
  SELECT MAX(_source_file)
  FROM raw.prices_1h
  """
  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(query)
      return cur.fetchone()[0]

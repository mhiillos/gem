from gem.db.connection import get_connection

def latest_timestamp():
  query = """
  SELECT MAX(timestamp)
  FROM fact_item
  """
  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(query)
      response = cur.fetchone()[0]

      if response is None:
        return 0

      return response.timestamp()


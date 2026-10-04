from gem.db.connection import get_connection

sql_items = """
INSERT INTO raw.items (id, examine, members, lowalch, buy_limit, value, highalch, icon, name, _source_file)
VALUES (%(id)s, %(examine)s, %(members)s, %(lowalch)s, %(buy_limit)s, %(value)s, %(highalch)s, %(icon)s, %(name)s, %(_source_file)s);
"""

sql_prices = """
INSERT INTO raw.prices_1h (item_id, window_timestamp, avg_high_price, high_price_volume, avg_low_price, low_price_volume, _source_file)
VALUES (%(item_id)s, %(window_timestamp)s, %(avg_high_price)s, %(high_price_volume)s, %(avg_low_price)s, %(low_price_volume)s, %(_source_file)s)
ON CONFLICT DO NOTHING;
"""

def load_prices(data):
  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.executemany(sql_prices, data)
    conn.commit()

def load_items(data):
  with get_connection() as conn:
    with conn.cursor() as cur:
      # Get rid of existing item metadata before loading new metadata
      cur.execute("TRUNCATE raw.items")
      cur.executemany(sql_items, data)
    conn.commit()


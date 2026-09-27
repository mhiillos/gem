from gem.db.connection import get_connection

sql_dim = """
INSERT INTO dim_item (item_id, name, high_alch, buy_limit)
VALUES (%(item_id)s, %(name)s, %(high_alch)s, %(buy_limit)s)
ON CONFLICT DO NOTHING;
"""

sql_fact = """
INSERT INTO fact_item (item_id, high_price, low_price, high_price_volume, low_price_volume, window_timestamp)
VALUES (%(item_id)s, %(high_price)s, %(low_price)s, %(high_price_volume)s, %(low_price_volume)s, %(window_timestamp)s)
ON CONFLICT DO NOTHING;
"""

def load(dim_entries, fact_entries):
  with get_connection() as conn:
    try:
      with conn.cursor() as cur:
        cur.executemany(sql_dim, dim_entries)
        cur.executemany(sql_fact, fact_entries)
      conn.commit()

    except Exception as e:
      conn.rollback()
      raise e


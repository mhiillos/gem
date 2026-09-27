-- Dimension table: Single item
CREATE TABLE IF NOT EXISTS dim_item (
  item_id INT PRIMARY KEY,
  name TEXT NOT NULL,
  high_alch INT NOT NULL,
  buy_limit INT NOT NULL
);

-- Fact table: information of an item's price and volume within a 1h window
CREATE TABLE IF NOT EXISTS fact_item (
  id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  item_id INT NOT NULL,
  high_price BIGINT,
  low_price BIGINT,
  high_price_volume INT NOT NULL,
  low_price_volume INT NOT NULL,
  window_timestamp TIMESTAMPTZ NOT NULL,

  FOREIGN KEY (item_id) REFERENCES dim_item(item_id) ON DELETE CASCADE,
  UNIQUE(item_id, window_timestamp)
);

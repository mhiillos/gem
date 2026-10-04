CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.prices_1h (
  item_id INT NOT NULL,
  window_timestamp TIMESTAMPTZ NOT NULL,
  avg_high_price NUMERIC,
  high_price_volume BIGINT,
  avg_low_price NUMERIC,
  low_price_volume BIGINT,
  _loaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  _source_file TEXT,

  UNIQUE (item_id, window_timestamp)
);

CREATE TABLE IF NOT EXISTS raw.items (
  id INT PRIMARY KEY,
  examine VARCHAR,
  members BOOLEAN,
  lowalch BIGINT,
  buy_limit INT,
  value BIGINT,
  highalch BIGINT,
  icon VARCHAR,
  name VARCHAR,
  _loaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  _source_file TEXT
);

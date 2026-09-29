WITH hours AS (
  SELECT generate_series(
    date_trunc('hour', NOW() - INTERVAL '7 days'),
    date_trunc('hour', NOW()),
    INTERVAL '1 hour'
  ) AS window_timestamp
),

prices AS (
  SELECT
    f.window_timestamp,
    f.high_price,
    f.low_price,
    f.high_price_volume + f.low_price_volume as volume
  FROM fact_item f
  JOIN dim_item d
    ON d.item_id = f.item_id
  WHERE d.name ILIKE %s
    AND f.window_timestamp >= date_trunc('hour', NOW() - INTERVAL '7 days')
)

SELECT
  h.window_timestamp,
  p.high_price,
  p.low_price,
  p.volume
FROM hours h
LEFT JOIN prices p
  ON p.window_timestamp = h.window_timestamp
ORDER BY h.window_timestamp;


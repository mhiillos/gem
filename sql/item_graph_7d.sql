WITH hours AS (
  SELECT generate_series(
    date_trunc('hour', NOW() - INTERVAL '7 days'),
    date_trunc('hour', NOW()),
    INTERVAL '1 hour'
  ) AS timestamp
),

prices AS (
  SELECT
    date_trunc('hour', f.timestamp) AS timestamp,
    MAX(f.price) FILTER (WHERE f.type = 'high') as high,
    MAX(f.price) FILTER (WHERE f.type = 'low') as low
  FROM fact_item f
  JOIN dim_item d
    ON d.item_id = f.item_id
  WHERE d.name ILIKE %s
    AND timestamp >= (NOW() - INTERVAL '7 days')
  GROUP BY date_trunc('hour', f.timestamp)
)

SELECT
  h.timestamp,
  p.high,
  p.low
FROM hours h
LEFT JOIN prices p
  ON p.timestamp = h.timestamp
ORDER BY h.timestamp;


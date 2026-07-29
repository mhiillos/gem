-- Checks against the latest update, and outputs the biggest price movers from 24 hours ago and 7 days ago (day and week). Output name,oldprice,newprice,change,pctchange
 WITH latest_high AS (
  SELECT DISTINCT ON (item_id)
    item_id,
    price AS high_price
  FROM fact_item
  WHERE type = 'high'
  ORDER BY item_id, timestamp DESC
),

latest_low AS (
  SELECT DISTINCT ON (item_id)
    item_id,
    price AS low_price
  FROM fact_item
  WHERE type = 'low'
  ORDER BY item_id, timestamp DESC
),

latest_mean AS (
SELECT
  d.item_id,
  (h.high_price + l.low_price) / 2 AS latest_price
FROM dim_item d
JOIN latest_high h
  ON d.item_id = h.item_id
JOIN latest_low l
  ON d.item_id = l.item_id
),

old_high AS (
  SELECT DISTINCT ON (item_id)
  item_id,
  price AS high_price
  FROM fact_item
  WHERE type = 'high'
    AND timestamp <= (
      SELECT MAX(timestamp) - INTERVAL '24 hours'
      FROM fact_item
    )
  ORDER BY item_id, timestamp DESC
),

old_low AS (
  SELECT DISTINCT ON (item_id)
  item_id,
  price AS low_price
  FROM fact_item
  WHERE type = 'low'
    AND timestamp <= (
      SELECT MAX(timestamp) - INTERVAL '24 hours'
      FROM fact_item
    )
  ORDER BY item_id, timestamp DESC
),

old_mean AS (
SELECT
  d.item_id,
  (h.high_price + l.low_price) / 2 AS old_price
FROM dim_item d
JOIN old_high h
  ON d.item_id = h.item_id
JOIN old_low l
  ON d.item_id = l.item_id
),

price_changes AS (
SELECT
  d.name,
  o.old_price,
  n.latest_price,
  (n.latest_price - o.old_price) AS diff,
  (n.latest_price - o.old_price) * 100.0 / o.old_price AS pct_diff
FROM dim_item d
JOIN old_mean o
  ON d.item_id = o.item_id
JOIN latest_mean n
 ON d.item_id = n.item_id
)

SELECT *
FROM price_changes
WHERE ABS(pct_diff) < 100
AND (old_price + latest_price) / 2 > 10000
ORDER BY pct_diff DESC;


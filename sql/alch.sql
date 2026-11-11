-- Checks alch value against current instant buy for potential profit, prioritizing high ROI items
select
  name,
  high_alch,
  high_price,
  high_price_at,
  alch_profit,
  buy_limit,
  total_volume_24h,
  alch_roi_pct
from dev_marts.mart_items_latest
where buy_limit >= 1000
and high_price_at >= (now() - interval '2 hour')
and total_volume_24h > 20000
order by alch_roi_pct desc nulls last
limit 50;

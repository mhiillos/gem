-- Latest high and low price per item, with the hour each was traded
select
  item_id,
  name,
  high_price,
  high_price_at,
  low_price,
  low_price_at,
  spread,
  mean_price,
  mean_price_at
from dev_marts.mart_items_latest
where mean_price is not null
order by name;

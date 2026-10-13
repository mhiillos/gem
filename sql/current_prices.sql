-- Latest high and low price per item, with the hour each was traded
select
  item_id,
  name,
  high_price,
  high_price_at,
  low_price,
  low_price_at,
  spread
from dev_marts.mart_items_latest
where high_price is not null
  or low_price is not null
order by name;

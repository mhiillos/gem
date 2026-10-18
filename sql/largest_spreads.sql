-- Calculates and filters spread data from daily data.
-- Filtering is done by using window pairs of low price and total volume
select
  i.name,
  d.low_price,
  d.high_price,
  d.spread,
  d.spread_pct,
  d.total_volume

from dev_marts.fct_prices_daily as d
join dev_marts.dim_items as i
  on i.item_id = d.item_id
where d.price_date = (select max(price_date) from dev_marts.fct_prices_daily)
and d.hours_traded > 12
and d.low_price >= 100
and d.total_volume >= case
  when d.low_price < 5000 then 25000
  when d.low_price < 20000 then 5000
  when d.low_price < 100000 then 500
  when (d.low_price < 1000000 and d.spread_pct > 50) then 10
  when d.low_price < 1000000 then 100
  else 5
end
order by d.spread_pct desc nulls last
limit 50;

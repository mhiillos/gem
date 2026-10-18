-- Biggest day-over-day mean_price movers on the newest complete UTC day traded in more than 12 hours, order by pct change. Low volume items are skipped (hours traded > 12)
select
  d.name,
  f.mean_price,
  f.mean_price_prev_day,
  f.mean_price_change_dod,
  f.mean_price_change_pct_dod,
  f.total_volume

from dev_marts.fct_prices_daily f
left join dev_marts.dim_items d
  on d.item_id = f.item_id
where f.hours_traded > 12
and f.price_date = (select max(price_date) from dev_marts.fct_prices_daily)
order by abs(f.mean_price_change_pct_dod) desc nulls last
limit 50;

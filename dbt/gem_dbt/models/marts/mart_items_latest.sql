with source as (

  select * from {{ ref('fct_prices') }}

),

items as (

  select * from {{ ref('dim_items') }}

),

ranked_high as (

  select
    *,
    row_number() over(
      partition by item_id
      order by
        window_timestamp desc
    ) as rn

  from source
  where high_price is not null

),

ranked_low as (

  select
    *,
    row_number() over(
      partition by item_id
      order by
        window_timestamp desc
    ) as rn

  from source
  where low_price is not null

),

latest_high as (

  select
    item_id,
    high_price,
    high_price_volume,
    window_timestamp as high_price_at

  from ranked_high
  where rn = 1

),

latest_low as (

  select
    item_id,
    low_price,
    low_price_volume,
    window_timestamp as low_price_at

  from ranked_low
  where rn = 1

),

ranked_mean as (

  select
    *,
    row_number() over(
      partition by item_id
      order by
        window_timestamp desc
    ) as rn

  from source
  where mean_price is not null

),

latest_mean as (

  select
    item_id,
    mean_price,
    window_timestamp as mean_price_at

  from ranked_mean
  where rn = 1

),

constants as (

  select
    mean_price as nature_rune_price,
    0.02 as ge_tax_rate,
    5000000 as ge_tax_cap
  from latest_mean
  where item_id = 561

),

volume_24h as (

  select
    item_id,
    sum(total_volume) as total_volume_24h

  from source
  where window_timestamp > (select max(window_timestamp) from source) - interval '24 hours'
  group by item_id

),

flip as (

  select
    latest_high.item_id,
    case when high_price_at = low_price_at
      then high_price - least(floor(ge_tax_rate * high_price), ge_tax_cap) - low_price
    end as flip_margin

  from latest_high
  left join latest_low on latest_low.item_id = latest_high.item_id
  cross join constants

),

final as (

  select
    items.item_id,
    name,
    icon_url,
    high_alch,
    buy_limit,
    high_price,
    high_price_at,
    high_price_volume,
    low_price,
    low_price_at,
    low_price_volume,
    case
      when high_price_at = low_price_at then (high_price - low_price)
    end as spread,
    mean_price,
    mean_price_at,
    coalesce(total_volume_24h, 0) as total_volume_24h,
    high_alch - high_price - nature_rune_price as alch_profit,
    (high_alch - high_price - nature_rune_price) / (high_price + nature_rune_price) * 100 as alch_roi_pct,
    flip_margin,
    flip_margin * buy_limit as flip_profit_per_limit,
    flip_margin / low_price * 100 as flip_roi_pct

  from items
  left join latest_high on latest_high.item_id = items.item_id
  left join latest_low on latest_low.item_id = items.item_id
  left join latest_mean on latest_mean.item_id = items.item_id
  left join volume_24h on volume_24h.item_id = items.item_id
  left join flip on flip.item_id = items.item_id
  cross join constants

)

select * from final

with source as (

  select * from {{ ref('stg_prices') }}

),

final as (

  select

    price_id,
    item_id,
    high_price,
    high_price_volume,
    low_price,
    low_price_volume,
    (coalesce(high_price * high_price_volume, 0) + coalesce(low_price * low_price_volume, 0))
      / nullif(high_price_volume + low_price_volume, 0) as mean_price,
    high_price_volume + low_price_volume as total_volume,
    high_price - low_price as spread,
    ((high_price - low_price) / low_price) * 100 as spread_pct,
    window_timestamp,

    -- Rolling 24h window price data
    sum(high_price * high_price_volume) over w_24h / nullif(sum(high_price_volume) over w_24h, 0) as high_price_avg_24h,
    sum(low_price * low_price_volume) over w_24h / nullif(sum(low_price_volume) over w_24h, 0) as low_price_avg_24h,
    sum(high_price_volume + low_price_volume) over w_24h as total_volume_24h,

    _loaded_at,
    _source_file

  from source
  window w_24h as (
    partition by item_id
    order by window_timestamp
    range between interval '23 hours' preceding and current row
  )

)

select * from final

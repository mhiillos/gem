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
    high_price_volume + low_price_volume as total_volume,
    high_price - low_price as spread,
    ((high_price - low_price) / low_price) * 100 as spread_pct,
    window_timestamp,
    _loaded_at,
    _source_file

  from source

)

select * from final

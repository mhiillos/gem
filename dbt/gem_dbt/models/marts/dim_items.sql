with source as (

  select * from {{ ref('stg_items') }}

),

final as (

  select
    item_id,
    examine,
    is_members,
    buy_limit,
    high_alch,
    'https://oldschool.runescape.wiki/images/' || replace(icon, ' ', '_') as icon_url,
    name,
    _loaded_at,
    _source_file

  from source

)

select * from final

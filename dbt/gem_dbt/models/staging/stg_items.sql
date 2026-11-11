with source as (

  select * from {{ source('gem','items') }}

),

renamed as (

  select
    id as item_id,
    examine,
    members as is_members,
    lowalch as low_alch,
    buy_limit,
    value,
    highalch as high_alch,
    icon,
    name,
    _loaded_at,
    _source_file

  from source

)

select * from renamed

-- Returns recoverable hour windows that are missing (4 days old)
{{ config(severity = 'warn') }}

with bounds as (

  select
    min(window_timestamp) as first_window,
    max(window_timestamp) as last_window
  from {{ ref('stg_prices') }}

),

expected as (

  select generate_series(first_window, last_window, interval '1 hour') as window_timestamp
  from bounds

),

loaded as (

  select distinct window_timestamp
  from {{ ref('stg_prices') }}

),

missing as (

  select window_timestamp
  from expected
  where not exists (
    select 1 from loaded
    where expected.window_timestamp = loaded.window_timestamp
  )

)

select window_timestamp
from missing
where window_timestamp > now() - interval '4 days'

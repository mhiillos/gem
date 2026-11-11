{% test price_null_when_no_volume(model, column_name, volume_column) %}

select *
from {{ model }}
where
  ({{ volume_column }} = 0 and {{ column_name }} is not null)
  or
  ({{ column_name }} is null and {{ volume_column }} != 0)

{% endtest %}

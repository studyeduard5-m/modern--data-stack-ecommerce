with source as (
    select * from {{ source('raw_cinema', 'views') }}
)

select
    view_id,
    subscriber_id,
    movie_id,
    watch_duration_min,
    cast(view_date as timestamp) as viewed_at
from source

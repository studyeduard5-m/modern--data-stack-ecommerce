with source as (
    select * from {{ source('raw_cinema', 'ratings') }}
)

select
    rating_id,
    subscriber_id,
    movie_id,
    cast(rating as integer) as rating,
    coalesce(comment, 'no comment') as comment
from source

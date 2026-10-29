with source as (
    select * from {{ source('raw_cinema', 'movies') }}
)

select
    movie_id,
    director_id,
    title,
    genre,
    release_year,
    duration_min
from source
where duration_min > 0

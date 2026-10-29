with source as (
    select * from {{ source('raw_cinema', 'directors') }}
)

select
    director_id,
    name as director_name,
    country,
    birth_year
from source

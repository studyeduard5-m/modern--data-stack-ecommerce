{{ config(materialized='table') }}

with stg_directors as (
    select * from {{ ref('stg_directors') }}
)

select
    director_id,
    director_name,
    country,
    birth_year
from stg_directors

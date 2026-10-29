{{ config(materialized='table') }}

with stg_ratings as (
    select * from {{ ref('stg_ratings') }}
),

stg_subscribers as (
    select * from {{ ref('stg_subscribers') }}
),

stg_movies as (
    select * from {{ ref('stg_movies') }}
)

select
    r.rating_id,
    r.subscriber_id,
    r.movie_id,
    r.rating,
    r.comment
from stg_ratings r
join stg_subscribers s on r.subscriber_id = s.subscriber_id
join stg_movies m on r.movie_id = m.movie_id

{{ config(materialized='table') }}

with stg_views as (
    select * from {{ ref('stg_views') }}
),

stg_subscribers as (
    select * from {{ ref('stg_subscribers') }}
),

stg_movies as (
    select * from {{ ref('stg_movies') }}
)

select
    v.view_id,
    v.subscriber_id,
    v.movie_id,
    v.watch_duration_min,
    m.duration_min,
    round(least(v.watch_duration_min::numeric / m.duration_min, 1) * 100, 2) as watch_percent,
    v.viewed_at
from stg_views v
join stg_subscribers s on v.subscriber_id = s.subscriber_id
join stg_movies m on v.movie_id = m.movie_id

with source as (
    select * from {{ source('raw_cinema', 'subscribers') }}
),

renamed_and_cleaned as (
    select
        subscriber_id,
        name as full_name,
        coalesce(email, 'unknown@example.com') as email,
        plan,
        cast(registration_date as date) as registration_date
    from source
)

select * from renamed_and_cleaned

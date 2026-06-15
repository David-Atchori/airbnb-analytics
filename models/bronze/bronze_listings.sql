{{ config(materialized='table') }}

SELECT
    id,
    listing_url,
    name,
    room_type,
    minimum_nights,
    host_id,
    price,
    created_at,
    updated_at
FROM read_csv_auto('https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/listings.csv',
                   header=true,
                   ignore_errors=true)

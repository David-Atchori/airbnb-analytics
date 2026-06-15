{{ config(materialized='table') }}

SELECT
    listing_id,
    date,
    reviewer_name,
    comments,
    sentiment
FROM read_csv_auto('https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/reviews.csv',
                   header=true,
                   ignore_errors=true)

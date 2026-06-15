{{ config(materialized='table') }}

SELECT
    full_moon_date
FROM read_csv_auto('https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/seed_full_moon_dates.csv',
                   header=true,
                   ignore_errors=true)

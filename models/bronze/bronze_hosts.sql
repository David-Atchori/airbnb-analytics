{{ config(materialized='table') }}

SELECT
    id,
    name,
    is_superhost,
    created_at,
    updated_at
FROM read_csv_auto('https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/hosts.csv',
                   header=true,
                   ignore_errors=true)

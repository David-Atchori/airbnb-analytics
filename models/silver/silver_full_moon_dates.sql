{{ config(materialized='table') }}

SELECT
    CAST(full_moon_date AS DATE) AS full_moon_date
FROM {{ ref('bronze_full_moon_dates') }}
WHERE full_moon_date IS NOT NULL

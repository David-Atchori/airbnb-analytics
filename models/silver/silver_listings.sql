{{ config(materialized='table') }}

SELECT
    CAST(id AS INTEGER)           AS listing_id,
    listing_url,
    name                          AS listing_name,
    room_type,
    CASE
        WHEN CAST(minimum_nights AS INTEGER) IS NULL OR CAST(minimum_nights AS INTEGER) <= 0 THEN 1
        ELSE CAST(minimum_nights AS INTEGER)
    END                           AS minimum_nights,
    CAST(host_id AS INTEGER)      AS host_id,
    CAST(REPLACE(REPLACE(price, '$', ''), ',', '') AS FLOAT) AS price,
    CAST(created_at AS TIMESTAMP) AS created_at,
    CAST(updated_at AS TIMESTAMP) AS updated_at
FROM {{ ref('bronze_listings') }}
WHERE id IS NOT NULL

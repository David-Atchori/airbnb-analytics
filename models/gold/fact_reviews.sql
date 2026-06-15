{{ config(materialized='table') }}

/*
  FACT_REVIEWS : Table de faits des avis clients.
  - Enrichissement avec l'indicateur pleine lune
  - Jointure avec les listings pour l'analyse combinée
*/

SELECT
    r.listing_id,
    r.review_date,
    r.reviewer_name,
    r.review_text,
    r.sentiment,
    CASE
        WHEN fm.full_moon_date IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS is_full_moon,
    l.listing_name,
    l.room_type,
    l.price,
    l.price_category,
    l.host_id,
    l.host_name,
    l.is_superhost,
    EXTRACT(YEAR  FROM r.review_date) AS review_year,
    EXTRACT(MONTH FROM r.review_date) AS review_month
FROM {{ ref('silver_reviews') }} r
LEFT JOIN {{ ref('silver_full_moon_dates') }} fm
    ON r.review_date = fm.full_moon_date + INTERVAL '1 day'
LEFT JOIN {{ ref('dim_listings') }} l
    ON r.listing_id = l.listing_id
ORDER BY r.review_date DESC

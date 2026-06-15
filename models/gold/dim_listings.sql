{{ config(materialized='table') }}

/*
  DIM_LISTINGS : Dimension annonces enrichie.
  - Catégorisation du prix en tranches
  - Jointure avec dim_hosts pour la dénormalisation
*/

SELECT
    l.listing_id,
    l.listing_url,
    l.listing_name,
    l.room_type,
    l.minimum_nights,
    l.price,
    CASE
        WHEN l.price < 50  THEN 'Budget'
        WHEN l.price < 150 THEN 'Standard'
        WHEN l.price < 300 THEN 'Premium'
        ELSE 'Luxury'
    END AS price_category,
    l.host_id,
    h.host_name,
    h.is_superhost,
    l.created_at,
    l.updated_at
FROM {{ ref('silver_listings') }} l
LEFT JOIN {{ ref('silver_hosts') }} h
    ON l.host_id = h.host_id

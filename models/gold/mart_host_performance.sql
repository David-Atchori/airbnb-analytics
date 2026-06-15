{{ config(materialized='table') }}

/*
  MART_HOST_PERFORMANCE : Performance des hôtes.
  KPIs par hôte : nombre de listings, nombre d'avis, sentiment moyen.
*/

SELECT
    host_id,
    host_name,
    is_superhost,
    COUNT(DISTINCT listing_id)                       AS nb_listings,
    COUNT(*)                                         AS total_reviews,
    ROUND(AVG(price), 2)                             AS avg_price,
    SUM(CASE WHEN sentiment = 'positive' THEN 1 ELSE 0 END) AS positive_reviews,
    SUM(CASE WHEN sentiment = 'negative' THEN 1 ELSE 0 END) AS negative_reviews,
    SUM(CASE WHEN sentiment = 'neutral'  THEN 1 ELSE 0 END) AS neutral_reviews,
    ROUND(
        SUM(CASE WHEN sentiment = 'positive' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0),
        2
    )                                                AS positive_rate_pct
FROM {{ ref('fact_reviews') }}
GROUP BY host_id, host_name, is_superhost
ORDER BY total_reviews DESC

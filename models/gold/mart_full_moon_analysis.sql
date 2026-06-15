{{ config(materialized='table') }}

/*
  MART_FULL_MOON_ANALYSIS : Data product agrégé.
  Compare la distribution des sentiments lors des nuits de pleine lune
  vs les autres nuits.
*/

SELECT
    is_full_moon,
    sentiment,
    COUNT(*)                                   AS nb_reviews,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY is_full_moon), 2) AS pct_sentiment
FROM {{ ref('fact_reviews') }}
WHERE sentiment IS NOT NULL
GROUP BY is_full_moon, sentiment
ORDER BY is_full_moon, sentiment

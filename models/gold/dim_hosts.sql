{{ config(materialized='table') }}

/*
  DIM_HOSTS : Dimension hôtes enrichie.
  - Calcul de l'ancienneté (jours depuis la création du compte)
  - Indicateur superhost mis en valeur
*/

SELECT
    host_id,
    host_name,
    is_superhost,
    created_at,
    updated_at,
    DATE_DIFF('day', created_at::DATE, CURRENT_DATE) AS host_seniority_days
FROM {{ ref('silver_hosts') }}

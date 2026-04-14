{{ config(
    materialized='table',
    unique_key='id'
) }}

SELECT 
    REPLACE(REPLACE(category::text, '{', ''), '}', '') AS category,
    count(*) as total_articles,
    count(DISTINCT source_id) as unique_sources
FROM {{ ref('staging') }} -- Notice we use ref() to point to your clean table
GROUP BY 1
ORDER BY 2 DESC
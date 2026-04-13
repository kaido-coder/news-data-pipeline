{{ config(
    materialized='table'
)}}

with clean_news as (
    SELECT * FROM {{ ref('staging') }} -- Notice we use ref() to point to your clean table
)

SELECT 
    source_id,
    category,
    COUNT(article_id) AS total_articles,
    MIN(pub_date) AS first_article_date,
    MAX(pub_date) AS latest_article_date
FROM clean_news
GROUP BY 1, 2
ORDER BY total_articles DESC
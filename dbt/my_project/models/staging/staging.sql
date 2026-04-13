{{ config(
    materialized='table',
    unique_key='id'
)}} 

with source as (
    select *
    from {{ source('dev', 'raw_news') }}
),
 cleaned_data as (
    select
        *,
        row_number() over (partition by article_id order by pub_date desc) as rn
    from source
)

SELECT
    id,
    article_id,
    title,
    description,
    pub_date,
    source_id,
    category,
    language,
    raw_json
FROM cleaned_data
WHERE rn = 1 AND title IS NOT NULL AND language = 'english'
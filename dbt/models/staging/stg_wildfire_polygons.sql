{{ config(
    materialized='table',
    cluster_by=['geometry']
) }}


WITH 

source AS (

    SELECT * from {{ source('staging', 'wildfire_polygons_raw') }}

),

transformed AS (

    SELECT
        DATE(DATETIME(TIMESTAMP(track_date),'America/Los_Angeles')) AS Track_date,
        CAST(geometry AS GEOGRAPHY) AS geometry,
        CAST(fire_link AS STRING) AS Fire_url,
        INITCAP(CAST(fire_stat AS STRING)) AS Fire_status,
        ROUND(CAST(fire_sz_ha AS FLOAT64),1) AS Fire_size_Ha,
        CAST(feature_cd AS STRING) AS Feature_code,
        CAST(fire_num AS STRING) AS Fire_number,
        CAST(objectid AS INT64) AS Object_ID

    FROM source

)

SELECT * FROM transformed

{{ config(materialized='view',cluster_by=['geometry']) }}

WITH 

source AS (

    SELECT * FROM {{ source('staging', 'recreation_lines_raw') }}

),

transformed AS (

    SELECT
        CAST(geometry AS GEOGRAPHY) AS geometry,
        CAST(objectid AS INT64) AS Object_ID,
        DATE(TIMESTAMP(PARSE_TIMESTAMP('%Y%m%d', CAST(proj_date AS STRING)))) AS Project_date,
        CAST(rmf_skey AS INT64) AS Feature_code,
        INITCAP(CAST(project_nm AS STRING)) AS Project_name,
        DATE(TIMESTAMP(PARSE_TIMESTAMP('%Y%m%d%H%M%S', CAST(retire_dt AS STRING)))) AS Retire_date ,
        CAST(feat_len AS FLOAT64) AS Feature_length_m,
        INITCAP(CAST(site_loc AS STRING)) AS Site_location,
        CAST(def_camps AS INT64) AS Campsites,
        INITCAP(CAST(life_st_cd AS STRING)) AS Trail_status,
        CAST(ffid AS STRING) AS Forest_file_ID,
        CAST(section_id AS STRING) AS Section_ID
    FROM source
)

SELECT * FROM transformed

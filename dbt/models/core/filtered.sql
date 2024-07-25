{{ config(
    materialized='table',
    cluster_by=['geometry']
)}}

SELECT
    r.geometry,
    r.Object_ID,
    r.Feature_code,
    r.Project_name,
    r.Feature_length_m,
    r.Site_location,
    r.Campsites,
    r.Trail_status,
    r.Forest_file_ID,
    r.Section_ID,
    f.Fire_number,
    f.Fire_size_Ha,
    f.Fire_status,
    f.Track_date
FROM
    {{ ref("stg_recreation_lines") }} as r
JOIN
    {{ ref("stg_wildfire_polygons") }} as f
ON
    ST_DWITHIN(r.geometry,f.geometry,30000)
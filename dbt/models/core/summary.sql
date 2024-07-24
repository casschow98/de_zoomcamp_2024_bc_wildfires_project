{{ config(
    materialized='table'
)}}


SELECT f.Project_name, COUNT(DISTINCT CASE WHEN f.fire_stat!='Out' THEN f.fire_num END) AS Nearby_active_fires,
COUNT(DISTINCT CASE WHEN f.fire_stat='Out' THEN f.fire_num END) AS Nearby_inactive_fires
FROM {{ ref("filtered") }} as f
GROUP BY f.Project_name
{{ config(
    materialized='table'
)}}


SELECT
    f.Project_name,
    COUNT(DISTINCT CASE WHEN f.Fire_status !='Out' THEN f.Fire_number END) AS Nearby_active_fires,
    COUNT(DISTINCT CASE WHEN f.Fire_status='Out' THEN f.Fire_number END) AS Nearby_inactive_fires
FROM
    {{ ref("filtered") }} as f
GROUP BY
    f.Project_name
ORDER BY
    f.Project_name ASC
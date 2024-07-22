{{ config(materialized='view',cluster_by=['geometry']) }}


with 

source as (

    select * from {{ source('staging', 'wildfire_polygons_raw') }}

),

limited as (

    select
        load_date,
        track_date,
        geometry,
        fire_link,
        versn_num,
        fire_stat,
        fire_sz_ha,
        fire_year,
        feature_cd,
        fire_num,
        objectid

    from source

)

select * from limited

{{ config(materialized='view') }}



with 

source as (

    select * from {{ source('staging', 'cchow_table') }}

),

renamed as (

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
        source,
        objectid

    from source

)

select * from renamed;

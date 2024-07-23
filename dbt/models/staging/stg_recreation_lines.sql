{{ config(materialized='view',cluster_by=['geometry']) }}

with 

source as (

    select * from {{ source('staging', 'recreation_lines_raw') }}

),

limited as (

    select
        geometry,
        objectid,
        feat_class,
        dist_nm,
        rec_vw_ind,
        proj_date,
        rmf_skey,
        project_nm,
        map_label,
        retire_dt,
        feat_len,
        feature_cd,
        project_tp,
        recdist_cd,
        site_loc,
        def_camps,
        applctn_sd,
        life_st_cd,
        ffid,
        rec_mf_cd,
        feat_lngth,
        rec_ft_cd,
        section_id,
        file_st_cd,        

    from source
)

select * from limited

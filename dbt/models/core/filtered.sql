{{ config(
    materialized='table',
    cluster_by=['geometry']
)}}

SELECT
    f.load_date,
    f.track_date,
    f.fire_link,
    f.versn_num,
    f.fire_stat,
    f.fire_sz_ha,
    f.fire_year,
    f.feature_cd as feature_cd_wf,
    f.fire_num,
    f.objectid as objectid_wf,
    r.objectid as objectid_rl,
    r.feat_class,
    r.dist_nm,
    r.rec_vw_ind,
    r.proj_date,
    r.dist_cd,
    r.rmf_skey,
    r.project_nm,
    r.map_label,
    r.retire_dt,
    r.feat_len,
    r.feature_cd as feature_cd_rl,
    r.project_tp,
    r.recdist_cd,
    r.site_loc,
    r.def_camps,
    r.applctn_sd,
    r.life_st_cd,
    r.ffid,
    r.rec_mf_cd,
    r.feat_lngth,
    r.rec_ft_cd,
    r.section_id,
    r.file_st_cd,
    r.geometry
FROM
    {{ ref("stg_recreation_lines") }} as r
JOIN
    {{ ref("stg_wildfire_polygons") }} as f
ON
    ST_DWITHIN(r.geometry,f.geometry,2000)
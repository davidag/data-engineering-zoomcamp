{{ config(materialized='table') }}

with
    fhv_data as (
        select *,
            'Fhv' as service_type
        from {{ ref('stg_fhv_tripdata') }}
    ),
    dim_zones as (
        select * from {{ ref('dim_zones') }}
        where borough != 'Unknown'
    )
select
    basenumid,

    pickup_datetime,
    pickup_locationid,
    pickup_zone.borough as pickup_borough,
    pickup_zone.zone as pickup_zone,

    dropoff_datetime,
    dropoff_locationid,
    dropoff_zone.borough as dropoff_borough,
    dropoff_zone.zone as dropoff_zone,

    sr_flag,
    affiliated_basenumid,
from fhv_data
inner join dim_zones as pickup_zone
on fhv_data.pickup_locationid = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on fhv_data.dropoff_locationid = dropoff_zone.locationid


select
    nid as node_id,
    uid as user_id,
    type as node_type,
    created,
    year,
    month,
    title,
    stems,
    view_counter

from {{ source('staging', 'nodes') }}

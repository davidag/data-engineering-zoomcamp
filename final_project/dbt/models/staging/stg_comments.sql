select
    cid as comment_id,
    nid as node_id,
    uid as user_id,
    type as comment_type,
    created,
    year,
    month,
    stems

from {{ source('staging', 'comments') }}

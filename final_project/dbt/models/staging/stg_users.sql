select
    uid as user_id,
    name as username,
    created,
    year,
    month

from {{ source('staging', 'users') }}

{{ config(materialized='table') }}

with user_nodes as (
    select
        user_id,
        year,
        month,
        node_type as type,
        count(node_id) as number_nodes,

    from {{ ref('stg_nodes') }}

    group by 1, 2, 3, 4
)
select
    user_id,
    user_nodes.year,
    user_nodes.month,
    user_nodes.type,
    coalesce(user_nodes.number_nodes, 0) as number_nodes,

from {{ ref('stg_users') }}

inner join user_nodes using (user_id)

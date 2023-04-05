{{ config(materialized='table') }}

with user_comments as (
    select
        user_id,
        year,
        month,
        comment_type as type,
        count(comment_id) as number_comments,

    from {{ ref('stg_comments') }}

    group by 1, 2, 3, 4
)
select
    user_id,
    username,
    user_comments.year,
    user_comments.month,
    user_comments.type,
    coalesce(user_comments.number_comments, 0) as number_comments,

from {{ ref('stg_users') }}

inner join user_comments using (user_id)

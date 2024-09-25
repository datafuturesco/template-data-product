
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

{{ config(materialized='table') }}

with first_data AS (

    select * 
    from {{ ref("dbt_poc", "first_name")}}

),

second_data AS (
    select * 
    from {{ ref("dbt_poc_a", "second_dbt_model")}}
)

select first_data.id, first_data.first_name,second_data.last_name
FROM first_data JOIN second_data
ON first_data.id = second_data.id

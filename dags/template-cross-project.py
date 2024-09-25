from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import pendulum
local_tz = pendulum.timezone('America/New_York')

DAG_ID = os.path.basename(__file__).replace(".py", "")

def dbt_run(selected_folder=None):
    import os
    import sys
    sys.path.insert(0, '/usr/local/airflow/dags/template-product-poc')
    from dbt_helpers import dbt_helpers
    import shutil
        
    current_dbt_path = '/usr/local/airflow/dags/template-product-poc/dbt'
    new_base_dbt_path = '/tmp/airflow/sample/test'
    
    # Remove the directory if it already exists
    if os.path.exists(new_base_dbt_path):
        shutil.rmtree(new_base_dbt_path)  # Deletes the directory and all its contents    
    
    # Create the directory again
    os.makedirs(new_base_dbt_path)
    
    new_target_dbt_path = dbt_helpers.move_dbt_project(current_dbt_path, new_base_dbt_path)
    os.chdir(new_target_dbt_path)
    dbt_helpers.list_files_in_directory(os.getcwd())

    dbt_helpers.run_dbt("debug")
    dbt_helpers.run_dbt("deps")
    if selected_folder:
        dbt_helpers.run_dbt("run", select=f"models/{selected_folder}")
    else:
        dbt_helpers.run_dbt("run")


# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(
    dag_id=DAG_ID,
        description="Run the DBT code.",
        start_date= datetime(2024,5,15, tzinfo=local_tz),  # Start date of the DAG
        schedule_interval = "25 7 * * *",
        catchup=False,
        concurrency=3, 
        max_active_runs=1,
)

# Task to run dbt
dbt_run_task = PythonVirtualenvOperator(
    task_id='dbt_run',
    python_callable=dbt_run,
    requirements=["dbt-snowflake==1.7.3"],
    system_site_packages=True,
    op_kwargs={'selected_folder': 'dbt_poc_child'},
    dag=dag,
)

dbt_run_task

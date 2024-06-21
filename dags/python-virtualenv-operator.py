from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator
from airflow.utils.dates import days_ago

def dbt_run():
    import os
    # Add project dags location to sys path to import the helper functions
    import sys
    sys.path.insert(0, '/usr/local/airflow/dags/template-data-product')
    from dbt_helpers import dbt_helpers
        
    # Define current and new dbt paths
    current_dbt_path = '/usr/local/airflow/dags/template-data-product/dbt'
    new_base_dbt_path = '/tmp/airflow'
    
    # Move dbt project to tmp directory
    new_target_dbt_path = dbt_helpers.move_dbt_project(current_dbt_path, new_base_dbt_path)
    # Listing files in tmp directory to verify dbt is copied correctly
    os.chdir(new_target_dbt_path)
    dbt_helpers.list_files_in_directory(os.getcwd())
    
    # Invoke dbt commands to run
    dbt_helpers.run_dbt("deps")
    dbt_helpers.run_dbt("run")

# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(
    'dbt_pythonvenv_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)

# Task to run dbt
dbt_run_task = PythonVirtualenvOperator(
    task_id='dbt_run',
    python_callable=dbt_run,
    requirements=["dbt-snowflake==1.7.3"],
    system_site_packages=True,
    dag=dag,
)

dbt_run_task

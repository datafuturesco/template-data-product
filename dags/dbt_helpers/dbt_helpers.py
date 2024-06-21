import os
import shutil
from dbt.cli.main import dbtRunner

# Copy the dbt project to a new tmp directory
def move_dbt_project(current_dbt_path, new_base_dbt_path):
    import os
    import shutil
    new_target_dbt_path = os.path.join(new_base_dbt_path, 'dbt')
    os.makedirs(new_base_dbt_path, exist_ok=True)
    try:
        shutil.move(current_dbt_path, new_target_dbt_path)
        print(f"Successfully moved DBT project from {current_dbt_path} to {new_target_dbt_path}")
    except Exception as e:
        print(f"Error moving DBT project: {e}")
    os.chdir(new_target_dbt_path)
    return new_target_dbt_path

# List the files in directory to verify 
def list_files_in_directory(directory):
    # import os
    os.chdir(directory)
    print("Current working directory after change:", os.getcwd())
    files = os.listdir()
    print("Files in the current working directory:")
    for file in files:
        print(file)

# Invoke dbt commands 
def run_dbt(command):
    # from dbt.cli.main import dbtRunner

    dbt = dbtRunner()
    cli_args = [command]
    res = dbt.invoke(cli_args)
    if res.success:
        print("Run Command successful")
        print(res)
    else:
        print("Run Command failed")
        print(res.exception)
    
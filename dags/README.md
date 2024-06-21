# DAGs

These are the tasks defined by Airflow which get run. Be sure to place whatever task you have created here.

The structure of dags folder is given below:

```text
├── dags/
│   └── dbt_helpers/
│      └── __init__.py
│      └── dbt_helpers.py
│   └── python-virtualenv-operator.py
|   └── template-data-product.py
```

#### template-data-product.py

This DAG enables dbt run using BashOperator.
When the MWAA environment is deployed using the custom requirements with dbt-snowflake or dbt-core, use this DAG to run dbt models.
**NOTE**: This DAG might fail if dbt-core is not part of the requirements.txt file used for MWAA deployment.

#### python-virtualenv-operator.py

If dbt-core is not a part of airflow and you want to run dbt models from DAG Runs, you can leverage the PythonVirtualenvOperator
to install the dbt in an Virtual environment and trigger dbt run from it.
Refer the `python-virtualenv-operator.py` for using PythonVirtualenvOperator to run dbt models.

This DAG imports helper functions defined in the `dbt_helpers.py` of dbt_helpers packaged folder.

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

## Cross-DAG Dependecies handling

We leveraged SNSPublish and SQSSensor operators of Airflow to achieve the cross-dag dependency.
Here is the breakdown on how you can use the sample DAGs provided in this module to create SNS topics and SQS queues using `boto3` client and subscribe to the SNS topic to receive messages in the SQS queue.

```text
├── dags/
│   └── create_sns_topic.py
│   └── create_sqs_queue.py
│   └── sns-publish-dag.py
│   └── sqs-sensor-dag.py
```

The placholders for the corresponding SNS and SQS variables breakdown is given below:

| Variable         | Description                                                                                                                                                      | Defined in file                         |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| <SNS_TOPIC_NAME> | This is for providing the SNS topic name you want to create. It is also used to set airflow variable for the sns topic, so provide a unique name for your topic. | create_sns_topic.py                     |
| <SNS_VARIABLE>   | This is used to retrieve the SNS topic arn from the airflow variable set while creating the topic. It is constructed as `<SNS_TOPIC_NAME> + _arn`                | sns-publish-dag.py, create-sqs-queue.py |
| <SQS_QUEUE_NAME> | Defines the SQS queue name to be created, provide a unique name as it is also used in creating the corresponding airflow variable.                               | create_sqs_queue.py                     |
| <SQS_VARIABLE>   | This is constructed as `<SQS_QUEUE_NAME> + _url`, defines the SQS queue url that is created using create_sqs_queue.py DAG                                        | sqs-sensor-dag.py                       |

#### create_sns_topic.py

This sample DAG creates SNS topic using boto3 client. Make sure to provide your topic name in the placeholder `<SNS_TOPIC_NAME>`.
The DAG also stores the topic arn as airflow variable `<SNS_VARIABLE>`which is used while subscribing to the topic created.

#### create_sqs_queue.py

This sample DAG creates SQS queue and also subscribes to the SNS topic.
It retrieves the SNS topic arn from the airflow variables provided in the `<SNS_VARIABLE>` to subscribe to it.
The created SQS queue url upon successful creation is also stored as airflow varibale, make sure to provide unique name to your queue in place of `<SQS_QUEUE_NAME>`.

#### sns-publish-dag.py

This DAG publishes to the SNS topic provided in the place of `<SNS_VARIABLE>` using SNSPublish operator upon successful upward dependent task runs.

#### sqs-sensor-dag.py

This is the DAG to enable cross-dag dependency, once the DAG tasks in the sns-publish-dag.py are successfully executed and the message is published to SNS topic,
SQS queues subscribed to the topic receive message. We use SQSSensor operator which waits for any such message to be received, once it reads the message from the queue provided in the place of `<SQS_VARIABLE>` it triggers the downward dependent tasks.

Useful links on how to use sns and sqs client to set various attributes :

- SNS client : https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html
- SQS client : https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html
- SNSPublish documentation : https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/operators/sns/index.html
- SQSSensor documentation : https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/sensors/sqs/index.html

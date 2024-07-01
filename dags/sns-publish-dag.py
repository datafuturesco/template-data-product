from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.operators.sns import SnsPublishOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
from datetime import datetime
import boto3

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

# Define DAG to publish a message to SNS topic after all upward tasks are successful
with DAG(
    'sns_publish_example',
    default_args=default_args,
    description='A simple DAG to publish a message to an SNS topic',
    schedule_interval=None,
    catchup=False
) as dag:

    # Dummy task to show upward dependenycy DAG run successful
    dummy_sleep_task = BashOperator(
        task_id='sleep_task',
        bash_command='sleep 10'
    )

    # SNS publish operator publishing message to the SNS topic set in the airflow variables
    publish_to_sns = SnsPublishOperator(
        task_id='publish_to_sns',
        target_arn=Variable.get("<SNS_VARIABLE>"),
        message='This is a test message from Airflow',
        subject='Test SNS Message'
    )

    dummy_sleep_task >> publish_to_sns

if __name__ == "__main__":
    dag.cli()

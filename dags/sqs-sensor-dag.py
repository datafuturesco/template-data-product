from airflow import DAG
from airflow.providers.amazon.aws.sensors.sqs import SqsSensor
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
from datetime import timedelta
import boto3

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

def print_sqs_message():
    print("Hello, SQS read and delete successful!! ")  
   
# Define DAG to receive messages from the SQS queue published by SNS topic
with DAG(
    'sqs_sensor_example',
    default_args=default_args,
    description='A simple DAG to sense and print messages from SQS',
    schedule_interval=None
) as dag:

    # SQS sensor waiting to receive message in the SQS queue provided in the airflow variable 
    sense_sqs_queue = SqsSensor(
        task_id='sense_sqs_queue',
        sqs_queue=Variable.get("<SQS_VARIABLE>"), # check for airflow variables and provide your preferred queue variable
        aws_conn_id='aws_default',
        max_messages=1,
        wait_time_seconds=20,
        visibility_timeout=30,
        mode='reschedule'
    )
    
    # Example task to show the cross dag dependency 
    print_message = PythonOperator(
        task_id='print_message',
        python_callable=print_sqs_message
    )

    sense_sqs_queue >> print_message

if __name__ == "__main__":
    dag.cli()

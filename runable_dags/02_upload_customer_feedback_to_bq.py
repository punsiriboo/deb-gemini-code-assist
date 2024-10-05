from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
import requests
import json
from datetime import datetime, timedelta
import os
import pandas as pd

# Replace with your values
PROJECT_ID = 'YOUR_PROJECT_ID'
BUCKET_NAME = 'deb-gemini-code-assist-YOUR_NAME'
DESTINATION_TABLE = 'gemini_assist_workshop.customer_feedback'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

def _extract_and_upload_to_gcs(**kwargs):
    """
    Extracts data from a JSON file, converts it to CSV, and uploads to GCS.
    """
    file_path = 'customer_feedback.json'
    folder_name = 'raw/customer_feedback'
    file_name = f'customer_feedback_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    gcs_file_path = f'{folder_name}/{file_name}'

    with open(file_path, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df.to_csv(f'/tmp/{file_name}', index=False)

    gcs_hook = GCSHook()
    gcs_hook.upload(bucket_name=BUCKET_NAME, object_name=gcs_file_path, filename=f'/tmp/{file_name}')

    return gcs_file_path

def _transform_data(**kwargs):
    """
    Reads data from GCS, performs transformations, and uploads the processed data back to GCS.
    """
    ti = kwargs['ti']
    input_file_path = ti.xcom_pull(task_ids='extract_and_upload_to_gcs')
    folder_name = 'processed/customer_feedback'
    file_name = f'customer_feedback_processed_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    output_file_path = f'{folder_name}/{file_name}'

    gcs_hook = GCSHook()
    file_content = gcs_hook.download(bucket_name=BUCKET_NAME, object_name=input_file_path)
    df = pd.read_csv(file_content)

    # Perform your data transformations here
    df['count_character'] = df['customer_review'].str.len()
    df['age_segment'] = df['age'].apply(lambda x: 'Young' if x < 30 else 'Adult' if x < 60 else 'Senior')

    df.to_csv(f'/tmp/{file_name}', index=False)
    gcs_hook.upload(bucket_name=BUCKET_NAME, object_name=output_file_path, filename=f'/tmp/{file_name}')

with DAG(
    'customer_feedback_pipeline',
    default_args=default_args,
    description='Processes customer feedback data and loads it to BigQuery',
    schedule_interval=None,  # Set your desired schedule
    catchup=False,
) as dag:

    extract_and_upload_task = PythonOperator(
        task_id='extract_and_upload_to_gcs',
        python_callable=_extract_and_upload_to_gcs,
        provide_context=True,
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=_transform_data,
        provide_context=True,
    )

    load_to_bigquery_task = GCSToBigQueryOperator(
        task_id='load_to_bigquery',
        bucket=BUCKET_NAME,
        source_objects=['processed/customer_feedback/*.csv'],
        destination_project_dataset_table=DESTINATION_TABLE,
        source_format='CSV',
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_APPEND',
        skip_leading_rows=1,
    )

    extract_and_upload_task >> transform_task >> load_to_bigquery_task 

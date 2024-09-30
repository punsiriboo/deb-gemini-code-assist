from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
import requests
import json
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

def _fetch_and_save_coingecko_data(**kwargs):
    """
    Fetches data from the CoinGecko API and saves it to Google Cloud Storage.
    """
    ti = kwargs['ti']
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether&vs_currencies=usd,thb&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true')
    data = response.json()
    
    bucket_name = 'de-data-th-gemini'
    folder_name = 'raw/coingecko'
    file_name = f'coingecko_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    file_path = f'{folder_name}/{file_name}'

    gcs_hook = GCSHook()
    gcs_hook.upload(bucket_name=bucket_name, object_name=file_path, data=json.dumps(data))

with DAG(
    'coingecko_data_pipeline',
    default_args=default_args,
    description='Collects crypto price data from CoinGecko API and loads it to BigQuery',
    schedule_interval=timedelta(hours=1),
    catchup=False,
) as dag:

    fetch_and_save_data = PythonOperator(
        task_id='fetch_and_save_coingecko_data',
        python_callable=_fetch_and_save_coingecko_data,
        provide_context=True,
    )

    load_data_to_bigquery = GCSToBigQueryOperator(
        task_id='load_data_to_bigquery',
        bucket='de-data-th-gemini',
        source_objects=['raw/coingecko/*.json'],
        destination_project_dataset_table='gemini-nt-test-2.coingecko.price',
        source_format='NEWLINE_DELIMITED_JSON',
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_APPEND',
    )

    fetch_and_save_data >> load_data_to_bigquery

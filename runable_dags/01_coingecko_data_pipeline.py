from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
import requests
import json
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'gemini-code-assist',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'coingecko_api_to_bigquery',
    default_args=default_args,
    description='Collect data from CoinGecko API and load to BigQuery',
    schedule_interval='0 0 * * 1,3,5',  # Run every Monday, Wednesday, and Friday at 00:00 (midnight)
    start_date=datetime(2023, 12, 18),
    catchup=False,
) as dag:

    # Task 1: Collect data from CoinGecko API
    def collect_coingecko_data(**kwargs):
        api_url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {
            'ids': 'bitcoin,ethereum,tether',
            'vs_currencies': 'usd,thb',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true',
            'include_24hr_change': 'true',
            'include_last_updated_at': 'true',
        }

        response = requests.get(api_url, params=params)
        data = response.json()

        # Convert timestamp to datetime object
        for coin, values in data.items():
            data[coin]['last_updated_at'] = datetime.fromtimestamp(values['last_updated_at']).isoformat()

        # Upload JSON data to GCS
        bucket_name = kwargs['bucket_name']
        gcs_folder = 'raw/coingecko'
        gcs_hook = GCSHook()
        gcs_hook.upload(
            bucket_name=bucket_name,
            object_name=f'{gcs_folder}/coingecko_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
            data=json.dumps(data),
        )

    collect_data_task = PythonOperator(
        task_id='collect_coingecko_data',
        python_callable=collect_coingecko_data,
        op_kwargs={'bucket_name': 'deb-gemini-code-assist-YOUR_NAME'},  # Replace with your bucket name
    )

    # Task 2: Load data from GCS to BigQuery
    load_to_bq_task = GCSToBigQueryOperator(
        task_id='load_to_bigquery',
        bucket='deb-gemini-code-assist-YOUR_NAME',  # Replace with your bucket name
        source_objects=['raw/coingecko/*.json'],  # Load all JSON files in the folder
        destination_project_dataset_table='gemini_assist_workshop.coingecko_price',
        write_disposition='WRITE_APPEND',  # Append data to the table
        source_format='NEWLINE_DELIMITED_JSON',
        create_disposition='CREATE_IF_NEEDED',  # Create the table if it doesn't exist
    )

    # Set task dependencies
    collect_data_task >> load_to_bq_task

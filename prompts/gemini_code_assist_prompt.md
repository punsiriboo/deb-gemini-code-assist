
# Gemini Code Assist for Data Engineering  - Prompt 

## DAG_1 - ingest data from API to BigQuery

```
Create Airflow DAG that contain 2 tasks:
Objective is to collect data and upload Create/Append to BigQuery Table 
projec_id=`YOUR_PROJECT_ID`
1. Collect Data from API using PythonOperator:
https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether&vs_currencies=usd,thb&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true
2. Save results in GSC 
bucket_name=`deb-gemini-code-assist-YOUR_NAME` 
folder=`raw/coingecko`
And then upload data from GSC to BigQuery
destination_project_dataset_table=`de_code_assist_workshop.coingecko_price`
```



## DAG_2 - ingest data from Json File to BigQuery

```
Create Airflow DAG that contain 3 tasks:
projec_id=`YOUR_PROJECT_ID`
bucket_name=`deb-gemini-code-assist-YOUR_NAME` 
destination_project_dataset_table=`de_code_assist_workshop.ecommerce_products`

1. Load data from path `csv_files/products.json` and convert to csv and upload to GCS 
folder=`raw/ecommerce_products`

2. Get data from raw and transform by adding new column

folder=`processed/ecommerce_products\`
```
from airflow import DAG
from airflow.utils.dates import days_ago
from airbyte_airflow_provider_advm.hook import AirbyteHook
from airflow.operators.python import PythonOperator

def print_hook_status():
    print(AirbyteHook(airbyte_conn_id='airbyte_default').test_connection())

with DAG(dag_id='sample_airbyte_hook_check',
         start_date=days_ago(1)
    ) as dag:
    PythonOperator(print_hook_status)
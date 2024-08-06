from airbyte_airflow_provider_advm.operators import AirbyteSourceConfigTransformOperator
from airflow import DAG
from datetime import datetime, timedelta


with DAG(
    dag_id="example_airbyte_operator",
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    dagrun_timeout=timedelta(minutes=60),
    tags=["example"],
    catchup=False,
) as dag:

    transform_source_config = AirbyteSourceConfigTransformOperator(
        task_id="airbyte_transform_source_config_example",
        source_id="15bc3800-82e4-48c3-a32d-620661273f28",
    )

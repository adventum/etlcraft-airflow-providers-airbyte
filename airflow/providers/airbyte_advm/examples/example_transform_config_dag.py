from airflow.providers.airbyte_advm.operators.airbyte import AirbyteSourceConfigTransformOperator, AirbyteTriggerSyncOperator
from airflow.providers.airbyte_advm.sensors.airbyte import AirbyteJobSensor
from airflow import DAG
from datetime import datetime, timedelta


with DAG(
    dag_id='example_airbyte_operator',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    dagrun_timeout=timedelta(minutes=60),
    tags=['example'],
    catchup=False,
) as dag:

    transform_source_config = AirbyteSourceConfigTransformOperator(
        task_id='airbyte_transform_source_config_example',
        source_id='15bc3800-82e4-48c3-a32d-620661273f28'
    )

    sync_source_destination = AirbyteTriggerSyncOperator(
        task_id='airbyte_sync_source_dest_example',
        connection_id='15bc3800-82e4-48c3-a32d-620661273f28',
    )
    # [END howto_operator_airbyte_synchronous]

    # [START howto_operator_airbyte_asynchronous]
    async_source_destination = AirbyteTriggerSyncOperator(
        task_id='airbyte_async_source_dest_example',
        connection_id='15bc3800-82e4-48c3-a32d-620661273f28',
        asynchronous=True,
    )

    airbyte_sensor = AirbyteJobSensor(
        task_id='airbyte_sensor_source_dest_example',
        airbyte_job_id=async_source_destination.output,
    )

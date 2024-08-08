from airbyte_airflow_provider_advm.hook import AirbyteHook
from airbyte_api.models import ConnectionsListRequest
from airflow import DAG
from airflow.utils.dates import datetime
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator

dag = DAG(
    dag_id="sync_airbyte_connections_by_prefix",
    start_date=datetime(2022, 9, 8),
    description="Run Sync Airbyte workspace non-deleted connections by their name prefix",
    schedule_interval="0 3 * * *",
)


def get_airbyte_connections_by_prefix(
    workspace_id: str, airbyte_conn_id: str, prefix: str, api_version: str = "v1"
):
    hook = AirbyteHook(airbyte_conn_id=airbyte_conn_id, api_version=api_version)
    workspace_connections = hook.list_connections(
        request=ConnectionsListRequest(workspace_id=workspace_id)
    )
    return list(filter(lambda conn: conn.prefix == prefix, workspace_connections))


connections = get_airbyte_connections_by_prefix(
    workspace_id="12345asdv-fab0-12345-8da0-123456abcde",
    airbyte_conn_id="default_airbyte_conn",
    prefix="my_prefix",
)

for connection in connections:
    AirbyteTriggerSyncOperator(
        dag=dag,
        connection_id=connection.connection_id,
        task_id=f"{connection.connection_id}__sync",
        airbyte_conn_id="default_airbyte_conn",
    )

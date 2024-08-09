import time
from typing import Any, Optional, Union

from airflow.exceptions import AirflowException
from airbyte_api.api import AirbyteApi
from airbyte_api.models import (
    ApiBaseModel,
    ConnectionsListRequest,
    GetJobRequest,
    JobStatus,
)
from airflow.providers.airbyte.hooks.airbyte import AirbyteHook as _AirbyteHook


class AirbyteHook(_AirbyteHook, AirbyteApi):
    """
    Hook for Airbyte API

    :param airbyte_conn_id: Required. The name of the Airflow connection to get
        connection information for Airbyte.
    :param api_version: Optional. Airbyte API version.
    """

    def __init__(
        self, airbyte_conn_id: str = "airbyte_default", api_version: str = "v1"
    ) -> None:
        super().__init__(airbyte_conn_id=airbyte_conn_id, api_version=api_version)
        self.api_version: str = api_version

    def _api_request(
        self, endpoint: str, data: ApiBaseModel = None, request_method: str = "POST"
    ) -> Any:
        self.method = request_method
        return self.run(
            endpoint=f"api/{self.api_version}/{endpoint}",
            json=(
                data.dict(exclude_none=True, exclude_unset=True, by_alias=True)
                if data
                else None
            ) if isinstance(data, ApiBaseModel) else data,
            headers={"accept": "application/json"},
        )

    def get_airbyte_connections_by_prefix(self, workspace_id: str, prefix: str):
        """Return Airbyte Connections filtered by prefix equals `prefix` arg"""
        workspace_connections = self.list_connections(
            request=ConnectionsListRequest(workspace_id=workspace_id)
        )
        return list(filter(lambda conn: conn.prefix == prefix, workspace_connections))

    def get_airbyte_connections_by_prefix_startswith(
        self, workspace_id: str, prefix_startswith: str
    ):
        """Return Airbyte Connections filtered by prefix startswith `prefix_startswith` arg"""
        workspace_connections = self.list_connections(
            request=ConnectionsListRequest(workspace_id=workspace_id)
        )
        return list(
            filter(
                lambda conn: conn.prefix.startswith(prefix_startswith),
                workspace_connections,
            )
        )

    def wait_for_job(
        self,
        job_id: Union[str, int],
        wait_seconds: float = 3,
        timeout: Optional[float] = 3600,
    ) -> None:
        """
        Helper method which polls a job to check if it finishes.

        :param job_id: Required. Id of the Airbyte job
        :param wait_seconds: Optional. Number of seconds between checks.
        :param timeout: Optional. How many seconds wait for job to be ready.
            Used only if ``asynchronous`` is False.
        """
        state = None
        start = time.monotonic()
        while True:
            if timeout and start + timeout < time.monotonic():
                raise AirflowException(
                    f"Timeout: Airbyte job {job_id} is not ready after {timeout}s"
                )
            time.sleep(wait_seconds)
            try:
                job = self.get_job(request=GetJobRequest(id=int(job_id)))
                state = job.job.status
            except AirflowException as err:
                self.log.info(
                    "Retrying. Airbyte API returned server error when waiting for job: %s",
                    err,
                )
                continue

            if state in (JobStatus.RUNNING, JobStatus.PENDING, JobStatus.INCOMPLETE):
                continue
            if state == JobStatus.SUCCEEDED:
                break
            if state == JobStatus.ERROR:
                raise AirflowException(f"Job failed:\n{job}")
            elif state == JobStatus.CANCELLED:
                raise AirflowException(f"Job was cancelled:\n{job}")
            else:
                raise Exception(
                    f"Encountered unexpected state `{state}` for job_id `{job_id}`"
                )

    def test_connection(self):
        """Tests the Airbyte connection by hitting the health API"""
        try:
            if self.health_check():
                return True, "Connection successfully tested"
            else:
                return False, "Health check false"
        except Exception as e:
            return False, str(e)

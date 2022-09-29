from typing import TYPE_CHECKING, Any, Dict, Sequence, Optional

from airflow.providers.airbyte_advm.hooks.airbyte import AirbyteHook
from airbyte_api.models import (CheckConnectionForUpdateRequest,
                                GetSourceRequest, SyncConnectionRequest, UpdateSourceRequest)
from airflow.models import BaseOperator

if TYPE_CHECKING:
    from airflow.utils.context import Context


class AirbyteSourceConfigTransformOperator(BaseOperator):
    template_fields: Sequence[str] = ('connection_id',)

    def __init__(
        self,
        *,
        airbyte_conn_id: str = "airbyte_default",
        source_id: str,
        config_patch: Dict[str, Any],
        api_version: str = "v1",
        check_config_connection: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.airbyte_conn_id = airbyte_conn_id
        self.source_id = source_id
        self.api_version = api_version
        self.check_config_connection = check_config_connection
        self.config_patch = config_patch

    def execute(self, context: 'Context') -> None:
        # Initiate Airbyte API Hook
        self.hook = AirbyteHook(
            airbyte_conn_id=self.airbyte_conn_id, api_version=self.api_version)

        # Get Source and it's config by Source ID
        source = self.hook.get_source(GetSourceRequest(
            source_id=self.source_id))

        current_source_config = source.connection_configuration
        current_source_config.update(self.config_patch)

        is_check_connection_succeeded = True
        if self.check_config_connection:
            is_check_connection_succeeded = self.hook.check_source_connection_for_update(
                request=CheckConnectionForUpdateRequest(
                    source_id=self.source_id,
                    connection_configuration=current_source_config,
                    name=source.name
                )
            ).job_info.succeeded

        if is_check_connection_succeeded:
            # Update config if succeeded
            return self.hook.update_source(
                request=UpdateSourceRequest(
                    source_id=self.source_id,
                    connection_configuration=current_source_config,
                    name=source.name
                )
            )


class AirbyteTriggerSyncOperator(BaseOperator):
    """
    This operator allows you to submit a job to an Airbyte server to run a integration
    process between your source and destination.

    .. seealso::
        For more information on how to use this operator, take a look at the guide:
        :ref:`howto/operator:AirbyteTriggerSyncOperator`

    :param airbyte_conn_id: Required. The name of the Airflow connection to get connection
        information for Airbyte.
    :param connection_id: Required. The Airbyte ConnectionId UUID between a source and destination.
    :param asynchronous: Optional. Flag to get job_id after submitting the job to the Airbyte API.
        This is useful for submitting long running jobs and
        waiting on them asynchronously using the AirbyteJobSensor.
    :param api_version: Optional. Airbyte API version.
    :param wait_seconds: Optional. Number of seconds between checks. Only used when ``asynchronous`` is False.
    :param timeout: Optional. The amount of time, in seconds, to wait for the request to complete.
        Only used when ``asynchronous`` is False.
    """

    template_fields: Sequence[str] = ('connection_id',)

    def __init__(
        self,
        connection_id: str,
        airbyte_conn_id: str = "airbyte_default",
        asynchronous: Optional[bool] = False,
        api_version: str = "v1",
        wait_seconds: float = 3,
        timeout: Optional[float] = 3600,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.airbyte_conn_id = airbyte_conn_id
        self.connection_id = connection_id
        self.timeout = timeout
        self.api_version = api_version
        self.wait_seconds = wait_seconds
        self.asynchronous = asynchronous

    def execute(self, context: 'Context') -> None:
        """Create Airbyte Job and wait to finish"""
        self.hook = AirbyteHook(
            airbyte_conn_id=self.airbyte_conn_id, api_version=self.api_version)
        job = self.hook.sync_connection(
            SyncConnectionRequest(connection_id=self.connection_id))
        self.job_id = job.job.id

        self.log.info("Job %s was submitted to Airbyte Server", self.job_id)
        if not self.asynchronous:
            self.log.info('Waiting for job %s to complete', self.job_id)
            self.hook.wait_for_job(
                job_id=self.job_id, wait_seconds=self.wait_seconds, timeout=self.timeout)
            self.log.info('Job %s completed successfully', self.job_id)

        return self.job_id

    def on_kill(self):
        """Cancel the job if task is cancelled"""
        if self.job_id:
            self.log.info('on_kill: cancel the airbyte Job %s', self.job_id)
            self.hook.cancel_job(self.job_id)

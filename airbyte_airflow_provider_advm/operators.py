from typing import TYPE_CHECKING, Any, Dict, Sequence, Optional

from airbyte_airflow_provider_advm.hook import AirbyteHook
from airbyte_api.models import (CheckConnectionForUpdateRequest,
                                GetSourceRequest, UpdateSourceRequest)
from airflow.models import BaseOperator

if TYPE_CHECKING:
    from airflow.utils.context import Context


class AirbyteSourceConfigTransformOperator(BaseOperator):
    template_fields: Sequence[str] = ('source_id',)

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

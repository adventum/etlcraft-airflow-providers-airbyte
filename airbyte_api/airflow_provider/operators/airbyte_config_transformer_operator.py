from datetime import datetime, timedelta
from typing import Any, Dict, Sequence
from airbyte_api.api import AirbyteApi
from airbyte_api.models import CheckConnectionForUpdateRequest, GetSourceRequest, UpdateSourceRequest
from jsonpath_ng import parse as jsonpath_parse, Child
from airbyte_api.airflow_provider.utils import today_date, n_days_ago_date
from airflow.models import BaseOperator


class AirbyteSourceConfigTransformOperator(BaseOperator):
    template_fields: Sequence[str] = ('connection_id',)

    def __init__(self, source_id: str, api: AirbyteApi):
        self.source = api.get_source(
            request=GetSourceRequest(source_id=source_id))
        self.api = api

    def update_source_config(self, config_patch: Dict[str, Any]):
        self.source.connection_configuration.update(config_patch)


def patch_update_source_config(source_id: str, config_patch: Dict[str, Any]):
    # Initiate Airbyte API Hook
    api = AirbyteApi(airbyte_url_base='http://localhost:8000/api/v1')

    # Get Source and it's config by Source ID
    source = api.get_source(GetSourceRequest(
        source_id=source_id))

    current_source_config = source.connection_configuration
    current_source_config.update(config_patch)

    # Check Connection for Source config with new generated dates
    is_check_connection_succeeded = api.check_source_connection_for_update(
        request=CheckConnectionForUpdateRequest(
            source_id=source_id,
            connection_configuration=current_source_config,
            name=source.name
        )
    ).job_info.succeeded

    if is_check_connection_succeeded:
        # Update config if succeeded
        return api.update_source(
            request=UpdateSourceRequest(
                source_id=source_id,
                connection_configuration=current_source_config,
                name=source.name
            )
        )


print(
    patch_update_source_config(
        source_id='a1db5c86-529b-4094-ae6f-70db9a9f31a0',
        config_patch={
            "date_from": today_date(),
            "date_to": n_days_ago_date(last_days_count=10)
        }
    )
)

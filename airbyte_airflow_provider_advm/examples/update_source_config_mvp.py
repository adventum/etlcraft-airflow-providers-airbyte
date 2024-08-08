from airbyte_api.api import AirbyteApi
from airbyte_api.models import (
    GetSourceRequest,
    CheckConnectionForUpdateRequest,
    UpdateSourceRequest,
)
from airbyte_airflow_provider_advm.utils import n_days_ago_date, today_date


source_id = ""
config_patch = {"date_from": n_days_ago_date(5), "date_to": today_date()}


# Initiate Airbyte API Hook
api = AirbyteApi(airbyte_url_base="http://localhost:8000/api/v1")

# Get Source and it's config by Source ID
source = api.get_source(GetSourceRequest(source_id=source_id))

current_source_config = source.connection_configuration
current_source_config.update(config_patch)

# Check Connection for Source config with new generated dates
is_check_connection_succeeded = api.check_source_connection_for_update(
    request=CheckConnectionForUpdateRequest(
        source_id=source_id,
        connection_configuration=current_source_config,
        name=source.name,
    )
).job_info.succeeded

if is_check_connection_succeeded:
    # Update config if succeeded
    api.update_source(
        request=UpdateSourceRequest(
            source_id=source_id,
            connection_configuration=current_source_config,
            name=source.name,
        )
    )

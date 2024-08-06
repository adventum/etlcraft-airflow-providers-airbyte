from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence
from copy import deepcopy

import json
from airflow import AirflowException
from airflow.models import BaseOperator
from jsonpath_ng import Child
from jsonpath_ng.ext import parse

from airbyte_airflow_provider_advm.hook import AirbyteHook
from airbyte_airflow_provider_advm.utils import (
    dates_format_pattern_mapping,
    first_level_date_from_field_names,
    first_level_date_to_field_names,
    lookup_fields_paths_mapping,
)
from airbyte_api.models import (
    CheckConnectionForUpdateRequest,
    DetailedJob,
    GetSourceRequest,
    ResetConnectionRequest,
    UpdateSourceRequest,
)

if TYPE_CHECKING:
    from airflow.utils.context import Context


class AirbyteSourceConfigTransformOperator(BaseOperator):
    template_fields: Sequence[str] = (
        "source_id",
        "config_patch",
    )

    def __init__(
        self,
        *,
        airbyte_conn_id: str = "airbyte_default",
        source_id: str,
        config_patch: Dict[str, Any],
        delete_fields: Optional[List[str]] = None,
        api_version: str = "v1",
        check_config_connection: bool = True,
        force_update: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.airbyte_conn_id = airbyte_conn_id
        self.source_id = source_id
        self.api_version = api_version
        self.check_config_connection = check_config_connection
        self.config_patch = config_patch
        self.delete_fields = delete_fields if delete_fields is not None else []
        self.force_update = force_update

    def execute(self, context: "Context") -> None:
        # Initiate Airbyte API Hook
        self.hook = AirbyteHook(
            airbyte_conn_id=self.airbyte_conn_id, api_version=self.api_version
        )

        # Get Source and it's config by Source ID
        source = self.hook.get_source(GetSourceRequest(source_id=self.source_id))

        current_source_config = source.connection_configuration
        current_config_initial = deepcopy(current_source_config)
        current_source_config.update(
            json.loads(self.config_patch)
            if isinstance(self.config_patch, str)
            else self.config_patch
        )

        if not self.force_update and current_source_config == current_config_initial:
            return

        for field_to_delete in self.delete_fields:
            try:
                del current_source_config[field_to_delete]
            except:
                pass

        is_check_connection_succeeded = True
        if self.check_config_connection:
            check_connection_job = self.hook.check_source_connection_for_update(
                request=CheckConnectionForUpdateRequest(
                    source_id=self.source_id,
                    connection_configuration=current_source_config,
                    name=source.name,
                )
            )
            is_check_connection_succeeded = check_connection_job.job_info.succeeded

        if is_check_connection_succeeded:
            # Update config if succeeded
            self.hook.update_source(
                request=UpdateSourceRequest(
                    source_id=self.source_id,
                    connection_configuration=current_source_config,
                    name=source.name,
                )
            )
        else:
            raise AirflowException()


class AirbyteResetConnectionOperator(BaseOperator):
    template_fields: Sequence[str] = ("source_id",)

    def __init__(
        self,
        *,
        airbyte_conn_id: str = "airbyte_default",
        connection_id: str,
        asynchronous: Optional[bool] = False,
        timeout: Optional[float] = 3600,
        wait_seconds: float = 3,
        api_version: str = "v1",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.airbyte_conn_id = airbyte_conn_id
        self.connection_id = connection_id
        self.timeout = timeout
        self.asynchronous = asynchronous
        self.wait_seconds = wait_seconds
        self.api_version = api_version

    def execute(self, context: "Context") -> None:
        # Initiate Airbyte API Hook
        self.hook = AirbyteHook(
            airbyte_conn_id=self.airbyte_conn_id, api_version=self.api_version
        )

        detailed_job: DetailedJob = self.hook.reset_connection(
            request=ResetConnectionRequest(connection_id=self.connection_id)
        )
        job_id = detailed_job.job.id
        self.log.info(
            f"Reset job {job_id} for connection {self.connection_id} was submitted to Airbyte Server"
        )
        if not self.asynchronous:
            self.log.info(f"Waiting for reset job {job_id} to complete")
            self.hook.wait_for_job(
                job_id=job_id, wait_seconds=self.wait_seconds, timeout=self.timeout
            )
            self.log.info(f"Job {job_id} completed successfully")

        return detailed_job.job.id


class LookupSourceDatesFieldsOperator(BaseOperator):
    custom_date_constants = ["custom_date"]
    default_date_format = "%Y-%m-%d"

    def __init__(
        self,
        *,
        airbyte_conn_id: str = "airbyte_default",
        source_id: str,
        date_from_jsonpath: Optional[str] = None,
        date_to_jsonpath: Optional[str] = None,
        date_type_constant_jsonpath: Optional[str] = None,
        api_version: str = "v1",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.airbyte_conn_id = airbyte_conn_id
        self.source_id = source_id
        self.api_version = api_version
        self.date_from_jsonpath = date_from_jsonpath
        self.date_to_jsonpath = date_to_jsonpath
        self.date_type_constant_jsonpath = date_type_constant_jsonpath

    @property
    def lookup_fields_paths_mapping(self):
        for df_fl_field_name, dt_fl_field_name in zip(
            first_level_date_from_field_names, first_level_date_to_field_names
        ):
            lookup_fields_paths_mapping["date_from"][
                f"$.{df_fl_field_name}"
            ] = f"$.{df_fl_field_name}"
            lookup_fields_paths_mapping["date_to"][
                f"$.{dt_fl_field_name}"
            ] = f"$.{dt_fl_field_name}"
            for const in self.custom_date_constants:
                lookup_fields_paths_mapping["date_from"][
                    f"$.date_range.oneOf[?(@.properties.date_range_type.const"
                    f" == '{const}')].properties.{df_fl_field_name}"
                ] = f"$.date_range.{df_fl_field_name}"
                lookup_fields_paths_mapping["date_to"][
                    f"$.date_range.oneOf[?(@.properties.date_range_type.const"
                    f" == '{const}')].properties.{dt_fl_field_name}"
                ] = f"$.date_range.{dt_fl_field_name}"
        return lookup_fields_paths_mapping

    def lookup_dates_fields(
        self,
        source_definition_spec: Dict[str, Any],
        skip_if_date_to_not_found: bool = True,
    ) -> Dict:
        spec_properties = source_definition_spec["properties"]

        found_field_paths_in_schema = {}
        for field_type in self.lookup_fields_paths_mapping.keys():
            found_jsonpath_pattern: Child = None
            for pattern in self.lookup_fields_paths_mapping[field_type].keys():
                jsonpath_pattern: Child = parse(pattern)
                if jsonpath_pattern.find(spec_properties):
                    found_field_paths_in_schema[field_type] = (
                        self.lookup_fields_paths_mapping[field_type][pattern]
                    )
                    if field_type == "date_type_const":
                        available_date_type_consts = [
                            found_const.value
                            for found_const in jsonpath_pattern.find(spec_properties)
                        ]
                        for const in self.custom_date_constants:
                            if const in available_date_type_consts:
                                found_field_paths_in_schema["custom_date_constant"] = (
                                    const
                                )
                    found_jsonpath_pattern = jsonpath_pattern

                    break

            if field_type not in found_field_paths_in_schema.keys():
                if field_type != "date_type_constant":
                    if field_type == "date_from" and not skip_if_date_to_not_found:
                        raise AirflowException(
                            f"{field_type} field not found in source defined specification."
                        )
            if (
                field_type in found_field_paths_in_schema.keys()
                and field_type == "date_from"
            ):
                date_from_field: Dict = found_jsonpath_pattern.find(spec_properties)[
                    0
                ].value
                found_field_paths_in_schema["date_format"] = None
                found_date_format_from_pattern = dates_format_pattern_mapping.get(
                    date_from_field.get("pattern")
                )

                if date_from_field.get("format") == "date-time":
                    found_field_paths_in_schema["date_format"] = (
                        self.default_date_format
                    )
                elif found_date_format_from_pattern:
                    found_field_paths_in_schema["date_format"] = (
                        found_date_format_from_pattern
                    )
                else:
                    found_field_paths_in_schema["date_format"] = (
                        self.default_date_format
                    )
        return found_field_paths_in_schema

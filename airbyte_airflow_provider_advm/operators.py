from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence
from copy import deepcopy

import json
import yaml
from airflow import AirflowException
from airflow.models import BaseOperator
from airflow.models import Variable
from jsonpath_ng import Child
from jsonpath_ng.ext import parse

from airbyte_airflow_provider_advm.hook import AirbyteHook
from airbyte_airflow_provider_advm.utils import (
    dates_format_pattern_mapping,
    first_level_date_from_field_names,
    first_level_date_to_field_names,
    lookup_fields_paths_mapping,
    etlcraft_variable,
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


class CollectConfigsOperator(BaseOperator):
    template_fields: Sequence[str] = ("config_names", "namespace")

    def __init__(
        self,
        *,
        config_names: Optional[list[str]] = None,
        namespace: Optional[str] = "etlcraft",
        entire_datacraft_variable: Optional[bool] = True,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.config_names = config_names if config_names else []
        self.namespace = namespace
        self.entire_datacraft_variable = entire_datacraft_variable

    def load_config(self, config_name: str) -> dict:
        source_key = f"source_for_config_{config_name}"
        format_key = f"format_for_config_{config_name}"
        path_key = f"path_for_config_{config_name}"

        source = etlcraft_variable(source_key, self.namespace, default_value="file")
        file_format = etlcraft_variable(format_key, self.namespace, default_value="yaml")
        path = etlcraft_variable(path_key, self.namespace, default_value=f"configs/{config_name}")

        if source == "file" and not path.endswith(('.json', '.yml', '.yaml')):
            extension = ".json" if file_format == "json" else ".yml"
            path += extension

        if source == "file":
            with open(path, 'r') as file:
                if file_format == "json":
                    config = json.load(file)
                else:
                    config = yaml.safe_load(file)
        elif source == "datacraft_variable":
            json_datacraft_variable = etlcraft_variable(config_name, self.namespace)
            if type(json_datacraft_variable) is str:
                json_datacraft_variable = json.loads(json_datacraft_variable)

            if self.entire_datacraft_variable:
                config = json_datacraft_variable
            else:
                config = json_datacraft_variable.get(path, {})
        elif source == "other_variable":
            other_variable_name = etlcraft_variable(f"value_for_config_{config_name}")
            config = Variable.get(path, default_var=other_variable_name)
            if file_format == "json":
                config = json.loads(config)
            else:
                config = yaml.safe_load(config)
        else:
            raise ValueError(f"Unknown source type: {source}")

        return config

    def execute(self, context: "Context") -> dict:
        all_configs = {}
        for config_name in self.config_names:
            all_configs[config_name] = self.load_config(config_name)

        return all_configs


class AirbyteGeneralOperator(BaseOperator):
    def __init__(
        self,
        *,
        airbyte_conn_id: str = "airbyte_default",
        endpoint: str,
        method: str = "POST",
        request_params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.airbyte_conn_id = airbyte_conn_id
        self.endpoint = endpoint
        self.method = method
        self.request_params = request_params or {}

    def execute(self, context: "Context") -> Any:
        self.log.info(f"Executing {self.method} request to {self.endpoint}")

        # Get Airbyte connection details
        hook = AirbyteHook(airbyte_conn_id=self.airbyte_conn_id)
        response = hook._api_request(
            endpoint=self.endpoint,
            data=self.request_params,
            request_method=self.method
        )

        if not response:
            raise AirflowException("Failed to get a valid response from Airbyte API")

        response_json = response.json()

        return response_json


class AirbyteCreateSourceOperator(BaseOperator):
    def __init__(
        self,
        *,
        airbyte_conn_id: str = "airbyte_default",
        source_definition_id: str,
        name: str,
        connection_configuration: Dict[str, Any],
        workspace_id: str,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.airbyte_conn_id = airbyte_conn_id
        self.source_definition_id = source_definition_id
        self.name = name
        self.connection_configuration = connection_configuration
        self.workspace_id = workspace_id

    def execute(self, context: "Context") -> Any:
        self.log.info(f"Creating Airbyte source {self.name}")

        hook = AirbyteHook(airbyte_conn_id=self.airbyte_conn_id)
        payload = {
            "sourceDefinitionId": self.source_definition_id,
            "connectionConfiguration": self.connection_configuration,
            "workspaceId": self.workspace_id,
            "name": self.name,
        }

        response = hook._api_request(
            endpoint="sources/create",
            data=payload,
            request_method="POST"
        )

        if not response:
            raise AirflowException("Failed to create source")

        response_json = response.json()

        return response_json


class AirbyteCreateDestinationOperator(BaseOperator):
    def __init__(
        self,
        *,
        airbyte_conn_id: str = "airbyte_default",
        destination_definition_id: str,
        name: str,
        connection_configuration: Dict[str, Any],
        workspace_id: str,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.airbyte_conn_id = airbyte_conn_id
        self.destination_definition_id = destination_definition_id
        self.name = name
        self.connection_configuration = connection_configuration
        self.workspace_id = workspace_id

    def execute(self, context: "Context") -> Any:
        self.log.info(f"Creating Airbyte destination {self.name}")

        hook = AirbyteHook(airbyte_conn_id=self.airbyte_conn_id)
        payload = {
            "destinationDefinitionId": self.destination_definition_id,
            "connectionConfiguration": self.connection_configuration,
            "workspaceId": self.workspace_id,
            "name": self.name,
        }

        response = hook._api_request(
            endpoint="destinations/create",
            data=payload,
            request_method="POST"
        )

        if not response:
            raise AirflowException("Failed to create destination")

        response_json = response.json()

        return response_json


class AirbyteCreateConnectionOperator(BaseOperator):
    def __init__(
        self,
        *,
        airbyte_conn_id: str = "airbyte_default",
        source_id: str,
        destination_id: str,
        sync_catalog: Dict[str, Any],
        status: Optional[str] = "active",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.airbyte_conn_id = airbyte_conn_id
        self.source_id = source_id
        self.destination_id = destination_id
        self.sync_catalog = sync_catalog
        self.status = status

    def execute(self, context: "Context") -> Any:
        self.log.info(f"Creating Airbyte connection from source to destination")

        hook = AirbyteHook(airbyte_conn_id=self.airbyte_conn_id)
        payload = {
            "sourceId": self.source_id,
            "destinationId": self.destination_id,
            "syncCatalog": self.sync_catalog,
            "status": self.status
        }

        response = hook._api_request(
            endpoint="connections/create",
            data=payload,
            request_method="POST"
        )

        if not response:
            raise AirflowException("Failed to create connection")

        response_json = response.json()

        return response_json


class AirbyteCreateSourceDefinitionOperator(BaseOperator):
    def __init__(
        self,
        *,
        airbyte_conn_id: str = "airbyte_default",
        source_definition: Dict[str, Any],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.airbyte_conn_id = airbyte_conn_id
        self.source_definition = source_definition

    def execute(self, context: "Context") -> Any:
        self.log.info(f"Creating Airbyte source definition")

        hook = AirbyteHook(airbyte_conn_id=self.airbyte_conn_id)
        response = hook._api_request(
            endpoint="source_definitions/create_custom",
            data=self.source_definition,
            request_method="POST"
        )

        if not response:
            raise AirflowException("Failed to create source definition")

        response_json = response.json()

        return response_json


class AirbyteCreateDestinationDefinitionOperator(BaseOperator):
    def __init__(
        self,
        *,
        airbyte_conn_id: str = "airbyte_default",
        destination_definition: Dict[str, Any],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.airbyte_conn_id = airbyte_conn_id
        self.destination_definition = destination_definition

    def execute(self, context: "Context") -> Any:
        self.log.info(f"Creating Airbyte destination definition")

        hook = AirbyteHook(airbyte_conn_id=self.airbyte_conn_id)
        response = hook._api_request(
            endpoint="destination_definitions/create_custom",
            data=self.destination_definition,
            request_method="POST"
        )

        if not response:
            raise AirflowException("Failed to create destination definition")

        response_json = response.json()

        return response_json


class AirbyteListConnectionsOperator(BaseOperator):
    def __init__(
        self,
        *,
        airbyte_conn_id: str = "airbyte_default",
        workspace_id: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.airbyte_conn_id = airbyte_conn_id
        self.workspace_id = workspace_id

    def execute(self, context: "Context") -> Any:
        self.log.info("Listing Airbyte connections")

        hook = AirbyteHook(airbyte_conn_id=self.airbyte_conn_id)
        request_params = {}
        if self.workspace_id:
            request_params["workspaceId"] = self.workspace_id

        response = hook._api_request(
            endpoint="connections/list",
            data=request_params,
            request_method="POST"
        )

        if not response:
            raise AirflowException("Failed to list connections")

        response_json = response.json()

        return response_json

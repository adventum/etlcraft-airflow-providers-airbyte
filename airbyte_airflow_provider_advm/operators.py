from typing import TYPE_CHECKING, Any, Dict, Mapping, Sequence, Optional

from airflow import AirflowException

from airbyte_airflow_provider_advm.hook import AirbyteHook
from airbyte_api.models import (CheckConnectionForUpdateRequest, GetSourceDefinitionSpecificationRequest,
                                GetSourceRequest, UpdateSourceRequest)
from airflow.models import BaseOperator

from jsonpath_ng import jsonpath, Child
from jsonpath_ng.ext import parse

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


class LookupSourceDatesFieldsOperator(BaseOperator):
    lookup_fields_paths_mapping = {
        'date_from': {
            '$.date_from': '$.date_from',
            '$.start_date': '$.start_date',
            '$.start_time': '$.start_time',
            '$.replication_start_date': '$.replication_start_date',
            '$.reports_start_date': '$.reports_start_date',
            '$.since':'$.since',
            '$.date_ranges_start_date': '$.date_ranges_start_date',
            "$.date_range.oneOf[?(@.properties.date_range_type.const"
            " == 'custom_date')].date_from": '$.date_range.date_from',
            "$.date_range.oneOf[?(@.properties.date_range_type.const"
            " == 'custom_date')].start_date": '$.date_range.start_date',
            "$.date_range.oneOf[?(@.properties.date_range_type.const"
            " == 'custom_date')].replication_start_date": '$.date_range.replication_start_date',
        },
        'date_to': {
            '$.date_to': '$.date_to',
            '$.end_date': '$.end_date',
            '$.replication_end_date': '$.replication_end_date',
            '$.reports_end_date': '$.reports_end_date',
            '$.end_time': '$.end_time',
            '$.date_ranges_end_date': '$.date_ranges_end_date',
            "$.date_range.oneOf[?(@.properties.date_range_type.const"
            " == 'custom_date')].properties.date_to": '$.date_range.date_to',
            "$.date_range.oneOf[?(@.properties.date_range_type.const"
            " == 'custom_date')].properties.end_date": '$.date_range.end_date',
            "$.date_range.oneOf[?(@.properties.date_range_type.const"
            " == 'custom_date')].properties.replication_end_date": '$.date_range.replication_end_date',
        
        },
        'date_type_constant': {
            '$.date_range.oneOf[*].properties.date_range_type.const': "$.date_range.date_range_type"
        },
        
    }
    custom_date_constants = ['custom_date']

    default_date_format = '%Y-%m-%d'
    dates_format_pattern_mapping = {
        "^[0-9]{4}-[0-9]{2}-[0-9]{2}$": "%Y-%m-%d",
        "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$": "%Y-%m-%dT%H:%M:%S%z"
    }

    def __init__(
        self,
        *,
        airbyte_conn_id: str = "airbyte_default",
        source_id: str,
        date_from_jsonpath: str | None = None,
        date_to_jsonpath: str | None = None,
        date_type_constant_jsonpath: str | None = None,
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
    
    def lookup_dates_fields(self, source_definition_spec: dict[str, Any]) -> Dict[str, str | None | Dict[str, str]]:
        spec_properties = source_definition_spec['properties']

        found_field_paths_in_schema = {}
        for field_type in self.lookup_fields_paths_mapping.keys():
            found_jsonpath_pattern: Child = None
            for pattern in self.lookup_fields_paths_mapping[field_type].keys():
                jsonpath_pattern: Child = parse(pattern)
                if jsonpath_pattern.find(spec_properties):
                    found_field_paths_in_schema[field_type] = self.lookup_fields_paths_mapping[field_type][pattern]
                    if field_type == 'date_type_const':
                        available_date_type_consts = [found_const.value for found_const in jsonpath_pattern.find(spec_properties)]
                        for const in self.custom_date_constants:
                            if const in available_date_type_consts:
                                found_field_paths_in_schema['custom_date_constant'] = const
                    found_jsonpath_pattern = jsonpath_pattern

                    break

            if field_type not in found_field_paths_in_schema.keys() and field_type != 'date_type_constant':
                raise AirflowException(f'{field_type} field not found in source defined specification.')
            if field_type in found_field_paths_in_schema.keys() and field_type == 'date_from':
                date_from_field: dict = found_jsonpath_pattern.find(spec_properties)[0]
                found_field_paths_in_schema['date_format'] = None
                found_date_format_from_pattern = self.dates_format_pattern_mapping.get(date_from_field.get('pattern'))
                if date_from_field.get('format') == 'date-time':
                    found_field_paths_in_schema['date_format'] = self.default_date_format
                elif found_date_format_from_pattern:
                    found_field_paths_in_schema['date_format'] = found_date_format_from_pattern
                else:
                    found_field_paths_in_schema['date_format'] = self.default_date_format



            

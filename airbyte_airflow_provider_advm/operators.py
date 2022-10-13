from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Sequence, Optional

from airflow import AirflowException

from airbyte_airflow_provider_advm.hook import AirbyteHook
from airbyte_api.models import (CheckConnectionForUpdateRequest, GetSourceDefinitionSpecificationRequest,
                                GetSourceRequest, UpdateSourceRequest)
from airflow.models import BaseOperator

from jsonpath_ng import jsonpath, Child
from jsonpath_ng.ext import parse

if TYPE_CHECKING:
    from airflow.utils.context import Context
from pprint import pprint

class AirbyteSourceConfigTransformOperator(BaseOperator):
    template_fields: Sequence[str] = ('source_id',)

    def __init__(
        self,
        *,
        airbyte_conn_id: str = "airbyte_default",
        source_id: str,
        config_patch: Dict[str, Any],
        delete_fields: List[str],
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
        self.delete_fields = delete_fields

    def execute(self, context: 'Context') -> None:
        # Initiate Airbyte API Hook
        self.hook = AirbyteHook(
            airbyte_conn_id=self.airbyte_conn_id, api_version=self.api_version)

        # Get Source and it's config by Source ID
        source = self.hook.get_source(GetSourceRequest(
            source_id=self.source_id))

        current_source_config = source.connection_configuration
        current_source_config.update(self.config_patch)

        for field_to_delete in self.delete_fields:
            try:
                del current_source_config[field_to_delete]
            except:
                pass

        is_check_connection_succeeded = True
        check_connection_job = None
        if self.check_config_connection:
            check_connection_job = self.hook.check_source_connection_for_update(
                request=CheckConnectionForUpdateRequest(
                    source_id=self.source_id,
                    connection_configuration=current_source_config,
                    name=source.name
                )
            )
            is_check_connection_succeeded = check_connection_job.job_info.succeeded

        if is_check_connection_succeeded:
            # Update config if succeeded
            self.hook.update_source(
                request=UpdateSourceRequest(
                    source_id=self.source_id,
                    connection_configuration=current_source_config,
                    name=source.name
                )
            )
        else:
            raise AirflowException()


class LookupSourceDatesFieldsOperator(BaseOperator):
    first_level_date_from_field_names = [
        'date_from',
        'start_date',
        'start_time',
        'replication_start_date',
        'reports_start_date',
        'since',
        'date_ranges_start_date'
    ]

    first_level_date_to_field_names = [
        'date_to',
        'end_date',
        'replication_end_date',
        'reports_end_date',
        'end_time',
        'date_ranges_end_date',
    ]

    custom_date_constants = ['custom_date']
    default_date_format = '%Y-%m-%d'
    dates_format_pattern_mapping = {
        "^[0-9]{4}-[0-9]{2}-[0-9]{2}$": "%Y-%m-%d",
        '^[0-9]{4}[0-9]{2}[0-9]{2}$': '%Y%m%d',
        '^$|^[0-9]{2}/[0-9]{2}/[0-9]{4}$': '%d/%m/%Y',
        '^$|^[0-9]{4}-[0-9]{2}-[0-9]{2}$': "%Y-%m-%d",
        '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$': '%Y-%m-%dT%H:%M:%SZ',
        '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}$': '%Y-%m-%dT%H:%M:%S',
        '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z?$': '%Y-%m-%dT%H:%M:%SZ',
        '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z|[0-9]{4}-[0-9]{2}-[0-9]{2}$': '%Y-%m-%dT%H:%M:%SZ',
        '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$': '%Y-%m-%dT%H:%M:%SZ',
        '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2}$': '%Y-%m-%dT%H:%M:%S+00:00',
        '^$|^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$': '%Y-%m-%dT%H:%M:%SZ',
        '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$|^$': '%Y-%m-%dT%H:%M:%SZ',
        '^[0-9]{4}-[0-9]{2}-[0-9]{2} ([0-9]{2}:[0-9]{2}:[0-9]{2})?$': "%Y-%m-%d %H:%M:%S%",
        '$|^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$': '%Y-%m-%d %H:%M:%S',
        '^$|^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}$': '%Y-%m-%dT%H:%M:%S',
        '^$|^[0-9]{4}-[0-9]{2}-[0-9]{2}( [0-9]{2}:[0-9]{2}:[0-9]{2})?$': '%Y-%m-%d %H:%M:%S',
        '^[0-9]{4}-[0-9]{2}-[0-9]{2}(T[0-9]{2}:[0-9]{2}:[0-9]{2}Z)?$': '%Y-%m-%dT%H:%M:%SZ',
        '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}Z$': lambda dt: dt.strftime('%Y-%m-%dT%H:%M:%S') + '.000Z',
        '^\\d{4}\\-(0[1-9]|1[012])\\-(0[1-9]|[12][0-9]|3[01])$': '%Y-%m-%d',
        '^(?:(\\d{4}\\-(0[1-9]|1[012])\\-(0[1-9]|[12][0-9]|3[01]))|)$': '%Y-%m-%d',
    }

    def __init__(
        self,
        *,
        airbyte_conn_id: str = "airbyte_default",
        source_id: str,
        date_from_jsonpath: Optional[str]= None,
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
        lookup_fields_paths_mapping = {
            'date_from': {},
            'date_to': {},
            'date_type_constant': {
                '$.date_range.oneOf[*].properties.date_range_type.const': "$.date_range.date_range_type"
            },
        }
        for df_fl_field_name, dt_fl_field_name in zip(
            self.first_level_date_from_field_names,
            self.first_level_date_to_field_names
        ):
            lookup_fields_paths_mapping['date_from'][
                f'$.{df_fl_field_name}'] = f'$.{df_fl_field_name}'
            lookup_fields_paths_mapping['date_to'][
                f'$.{dt_fl_field_name}'] = f'$.{dt_fl_field_name}'
            for const in self.custom_date_constants:
                lookup_fields_paths_mapping['date_from'][
                    f"$.date_range.oneOf[?(@.properties.date_range_type.const"
                    f" == '{const}')].properties.{df_fl_field_name}"
                ] = f'$.date_range.{df_fl_field_name}'
                lookup_fields_paths_mapping['date_to'][
                    f"$.date_range.oneOf[?(@.properties.date_range_type.const"
                    f" == '{const}')].properties.{dt_fl_field_name}"
                ] = f'$.date_range.{dt_fl_field_name}'
        return lookup_fields_paths_mapping
            
    
    def lookup_dates_fields(
        self,
        source_definition_spec: Dict[str, Any],
        skip_if_date_to_not_found: bool = True
    ) -> Dict:
        spec_properties = source_definition_spec['properties']

        found_field_paths_in_schema = {}
        for field_type in self.lookup_fields_paths_mapping.keys():
            found_jsonpath_pattern: Child = None
            for pattern in self.lookup_fields_paths_mapping[field_type].keys():
                jsonpath_pattern: Child = parse(pattern)
                if jsonpath_pattern.find(spec_properties):
                    found_field_paths_in_schema[
                        field_type
                    ] = self.lookup_fields_paths_mapping[field_type][pattern]
                    if field_type == 'date_type_const':
                        available_date_type_consts = [
                            found_const.value for found_const
                            in jsonpath_pattern.find(spec_properties)
                        ]
                        for const in self.custom_date_constants:
                            if const in available_date_type_consts:
                                found_field_paths_in_schema['custom_date_constant'] = const
                    found_jsonpath_pattern = jsonpath_pattern

                    break

            if field_type not in found_field_paths_in_schema.keys():
                if field_type != 'date_type_constant':
                    if field_type == 'date_from' and not skip_if_date_to_not_found:
                        raise AirflowException(f'{field_type} field not found in source defined specification.')
            if \
                field_type in found_field_paths_in_schema.keys() \
                    and field_type == 'date_from':
                date_from_field: Dict = found_jsonpath_pattern.find(spec_properties)[0].value
                found_field_paths_in_schema['date_format'] = None
                found_date_format_from_pattern = self.dates_format_pattern_mapping.get(
                    date_from_field.get('pattern')
                )
                
                if date_from_field.get('format') == 'date-time':
                    found_field_paths_in_schema['date_format'] = self.default_date_format
                elif found_date_format_from_pattern:
                    found_field_paths_in_schema['date_format'] = found_date_format_from_pattern
                # elif found_date_format_from_description:
                #     found_field_paths_in_schema['date_format'] = found_date_format_from_description
                else:
                    found_field_paths_in_schema['date_format'] = self.default_date_format
        return found_field_paths_in_schema



            

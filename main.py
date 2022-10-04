import json
from typing import TYPE_CHECKING, Any, Dict, Mapping, Sequence, Optional

from airflow import AirflowException

from airbyte_airflow_provider_advm.hook import AirbyteHook
from airbyte_api.api import AirbyteApi
from airbyte_api.models import (CheckConnectionForUpdateRequest, ConnectionsListRequest, GetSourceDefinitionRequest, GetSourceDefinitionSpecificationRequest,
                                GetSourceRequest, UpdateSourceRequest, Workspace)
from airflow.models import BaseOperator

from jsonpath_ng import jsonpath, Child
from jsonpath_ng.ext import parse

if TYPE_CHECKING:
    from airflow.utils.context import Context

class LookupSourceDatesFieldsOperator:
    lookup_fields_paths_mapping = {
        'date_from': {
            '$.date_from': '$.date_from',
            '$.start_date': '$.start_date',
            '$.start_time': '$.start_time',
            '$.replication_start_date': '$.replication_start_date',
            '$.start_datetime': '$.start_datetime',
            "$.date_range.oneOf[?(@.properties.date_range_type.const"
            " == 'custom_date')].properties.date_from": '$.date_range.date_from',
            "$.date_range.oneOf[?(@.properties.date_range_type.const"
            " == 'custom_date')].properties.start_date": '$.date_range.start_date',
            "$.date_range.oneOf[?(@.properties.date_range_type.const"
            " == 'custom_date')].properties.replication_start_date": '$.date_range.replication_start_date',
        },
        'date_to': {
            '$.date_to': '$.date_to',
            '$.end_date': '$.end_date',
            '$.replication_end_date': '$.replication_end_date',
            '$.end_time': '$.end_time',
            "$.date_range.oneOf[?(@.properties.date_range_type.const"
            " == 'custom_date')].properties.date_to": '$.date_range.date_to',
            "$.date_range.oneOf[?(@.properties.date_range_type.const"
            " == 'custom_date')].properties.end_date": '$.date_range.end_date',
            "$.date_range.oneOf[?(@.properties.date_range_type.const"
            " == 'custom_date')].properties.replication_end_date": '$.date_range.replication_end_date',
        
        },
        'date_type_constant': {
            '$.date_range.oneOf[*].properties.date_range_type.const': "$.date_range.date_range_type"
        }
    }
    custom_date_constants = ['custom_date']

    def __init__(
        self,
        *,
        airbyte_conn_id: str = "airbyte_default",
        source_id: str,
        date_from_jsonpath: str | None = None,
        date_to_jsonpath: str | None = None,
        date_type_constant_jsonpath: str | None = None,
        api_version: str = "v1",
        fail_on_fields_not_found: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.airbyte_conn_id = airbyte_conn_id
        self.source_id = source_id
        self.api_version = api_version
        self.date_from_jsonpath = date_from_jsonpath
        self.date_to_jsonpath = date_to_jsonpath
        self.date_type_constant_jsonpath = date_type_constant_jsonpath
        self.fail_on_fields_not_found = fail_on_fields_not_found

    def lookup_dates_fields(self, source_definition_spec: dict[str, Any]) -> Dict[str, str | None | Dict[str, str]]:
        spec_properties = source_definition_spec['properties']

        found_field_paths_in_schema = {}
        for field_type in self.lookup_fields_paths_mapping.keys():
            for pattern in self.lookup_fields_paths_mapping[field_type].keys():
                jsonpath_pattern: Child = parse(pattern)
                if jsonpath_pattern.find(spec_properties):
                    found_field_paths_in_schema[field_type] = self.lookup_fields_paths_mapping[field_type][pattern]
                    if field_type == 'date_type_constant':
                        available_date_type_consts = [
                            found_const.value for found_const
                            in jsonpath_pattern.find(spec_properties)
                        ]
                        print('available_date_type_consts', available_date_type_consts)
                        for const in self.custom_date_constants:
                            if const in available_date_type_consts:
                                found_field_paths_in_schema['custom_date_constant'] = const

                    break
            if field_type not in found_field_paths_in_schema.keys() \
            and field_type != 'date_type_constant' and self.fail_on_fields_not_found:
                raise Exception(f'{field_type} field not found in source defined specification.')
        
        return found_field_paths_in_schema


def main():
    op = LookupSourceDatesFieldsOperator(source_id=';')
    api = AirbyteHook(airbyte_conn_id='')
    workspace = api.list_workspaces()[0]
    prefix = '123'
    conns = api.list_connections(request=ConnectionsListRequest(workspace_id=workspace.workspace_id))
    for conn in conns:
        if conn.prefix == prefix:
            print(conn)
    


if __name__ == '__main__':
    main()
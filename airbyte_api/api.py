import json
from pprint import pprint
from typing import Optional

import requests
from requests.auth import HTTPBasicAuth
from .models import (ApiBaseModel, CheckConnectionForUpdateRequest,
                     CheckConnectionStatus,
                     CheckDestinationConnectionForUpdateRequest,
                     CheckDestinationConnectionRequest,
                     CheckSourceConnectionRequest, CloneDestinationRequest,
                     CloneSourceRequest, Connection, ConnectionsListRequest,
                     ConnectionState,
                     CreateCustomSourceDefinitionForWorkspaceRequest,
                     CreateDestinationDefinitionRequest,
                     CreateDestinationRequest,
                     CreateOrUpdateConnectionStateRequest,
                     CreateSourceDefinitionRequest, CreateSourceRequest,
                     DeleteConnectionRequest,
                     DeleteCustomSourceDefinitionForWorkspaceRequest,
                     DeleteDestinationDefinitionRequest,
                     DeleteDestinationRequest, DeleteSourceDefinitionRequest,
                     DeleteSourceRequest, Destination, DestinationDefinition,
                     DestinationDefinitionSpecification, DetailedJob,
                     DiscoverSourceSchemaRequest, GetConnectionRequest,
                     GetConnectionStateRequest, GetConnectionStateTypeRequest,
                     GetDestinationDefinitionRequest,
                     GetDestinationDefinitionSpecificationRequest,
                     GetDestinationRequest,
                     GetSourceDefinitionForWorkspaceRequest,
                     GetSourceDefinitionRequest,
                     GetSourceDefinitionSpecificationRequest, GetSourceRequest,
                     GrantPrivateSourceDefinitionForWorkspaceRequest, Job,
                     ListAllConnectionRequest, ListDestinationsRequest, ListJobsRequest,
                     ListPrivateDestinationDefinitionRequest,
                     ListPrivateSourceDefinitionRequest,
                     ListSourceDefinitionForWorkspaceRequest,
                     ListWorkspaceSourcesRequest, PrivateSourceDefinition,
                     ResetConnectionRequest, SearchConnectionsRequest,
                     SearchDestinationsRequest, SearchSourceRequest, Source,
                     SourceDefinition, SourceDefinitionSpecification,
                     SourceDiscoverSchemaJob, SyncConnectionRequest,
                     UpdateConnectionRequest,
                     UpdateCustomSourceDefinitionForWorkspaceRequest,
                     UpdateDestinationDefinitionRequest,
                     UpdateDestinationRequest, UpdateSourceDefinitionRequest,
                     UpdateSourceRequest, Workspace, GetJobRequest, CancelJobRequest)


class AirbyteApi:
    def __init__(self, airbyte_url_base: str = 'http://localhost:8000/api/v1', auth: Optional[HTTPBasicAuth] = None):
        self.airbyte_api_url = airbyte_url_base
        self.session = requests.Session()
        if auth:
            self.session.auth = auth

    def _api_request(
        self,
        endpoint: str,
        data: ApiBaseModel = None,
        request_method: str = 'POST'
    ) -> requests.Response:
        response = self.session.request(
            method=request_method,
            url=f'{self.airbyte_url_base}/{endpoint}',
            json=data.dict(
                exclude_none=True,
                exclude_unset=True,
                by_alias=True
            ) if data else None
        )
        try:
            response.raise_for_status()
        except:
            raise Exception(response.text)
        with open('resp.json', 'w') as f:
            json.dump(response.json(), f)
        return response

    def health_check(self) -> bool:
        return self._api_request(
            endpoint='health',
            request_method='GET'
        ).json()['available']

    def list_workspaces(
        self
    ) -> list[Workspace]:
        """ List all workspaces registered in the current Airbyte deployment """
        return [
            Workspace.parse_obj(source_definition_obj)
            for source_definition_obj in self._api_request(
                'workspaces/list'
            ).json()['workspaces']
        ]

    def create_source_definition(
        self,
        request: CreateSourceDefinitionRequest
    ) -> SourceDefinition:
        """ Creates a sourceDefinition """
        return SourceDefinition.parse_obj(
            self._api_request(
                'source_definitions/create',
                data=request
            ).json()
        )

    def update_source_definition(
        self,
        request: UpdateSourceDefinitionRequest
    ) -> SourceDefinition:
        """ 
        Update the SourceDefinition. Currently, the only allowed attribute to 
        update is the default docker image version. 
        """
        return SourceDefinition.parse_obj(
            self._api_request(
                'source_definitions/update',
                data=request
            ).json()
        )

    def list_source_definitions(self) -> list[SourceDefinition]:
        """
        List all the sourceDefinitions the current Airbyte deployment is configured to use
        """
        return [
            SourceDefinition.parse_obj(source_definition_obj)
            for source_definition_obj in self._api_request(
                'source_definitions/list'
            ).json()['sourceDefinitions']
        ]

    def list_latest_source_definitions(self) -> list[SourceDefinition]:
        """
        List the latest sourceDefinitions Airbyte supports.
        Guaranteed to retrieve the latest information on supported sources.
        """
        return [
            SourceDefinition.parse_obj(source_definition_obj)
            for source_definition_obj in self._api_request(
                'source_definitions/list_latest'
            ).json()['sourceDefinitions']
        ]

    def get_source_definition(
        self,
        request: GetSourceDefinitionRequest
    ) -> SourceDefinition:
        """ Get source definition """
        return SourceDefinition.parse_obj(
            self._api_request(
                'source_definitions/get',
                data=request
            ).json()
        )

    def delete_source_definition(
        self,
        request: DeleteSourceDefinitionRequest
    ) -> SourceDefinition:
        """
        Delete a source definition
        """
        return SourceDefinition.parse_obj(
            self._api_request(
                'source_definitions/delete',
                data=request
            ).json()
        )

    def list_private_source_definitions(
        self,
        request: ListPrivateSourceDefinitionRequest
    ) -> list[PrivateSourceDefinition]:
        """
        List all private, non-custom sourceDefinitions, and
        for each indicate whether the given workspace has a grant
        for using the definition
        """
        return [
            PrivateSourceDefinition.parse_obj(private_source_definition_obj)
            for private_source_definition_obj in self._api_request(
                'source_definitions/list_private',
                data=request
            ).json()['sourceDefinitions']
        ]

    def list_source_definitions_for_workspace(
        self,
        request: ListSourceDefinitionForWorkspaceRequest
    ) -> list[SourceDefinition]:
        """ List all the sourceDefinitions the given workspace is configured to use """
        return [
            SourceDefinition.parse_obj(source_definition_obj)
            for source_definition_obj in self._api_request(
                'source_definitions/list_for_workspace',
                data=request
            ).json()['sourceDefinitions']
        ]

    def create_custom_source_definition_for_workspace(
        self,
        request: CreateCustomSourceDefinitionForWorkspaceRequest
    ) -> SourceDefinition:
        """ Creates a custom sourceDefinition for the given workspace """
        return SourceDefinition.parse_obj(
            self._api_request(
                'source_definitions/create_custom',
                data=request
            ).json()
        )

    def get_source_definition_for_workspace(
        self,
        request: GetSourceDefinitionForWorkspaceRequest
    ) -> SourceDefinition:
        """ Get a sourceDefinition that is configured for the given workspace """
        return SourceDefinition.parse_obj(
            self._api_request(
                'source_definitions/get_for_workspace',
                data=request
            ).json()
        )

    def update_custom_source_definition_for_workspace(
        self,
        request: UpdateCustomSourceDefinitionForWorkspaceRequest
    ) -> SourceDefinition:
        """ Update a custom sourceDefinition for the given workspace """
        return SourceDefinition.parse_obj(
            self._api_request(
                'source_definitions/update_custom',
                data=request
            ).json()
        )

    def delete_custom_source_definition_for_workspace(
        self, request: DeleteCustomSourceDefinitionForWorkspaceRequest
    ) -> None:
        """ Delete a custom source definition for the given workspace """
        self._api_request(
            'source_definitions/delete_custom',
            data=request
        ).json()

    def grant_private_source_definition_for_workspace(
        self,
        request: GrantPrivateSourceDefinitionForWorkspaceRequest
    ) -> PrivateSourceDefinition:
        """ Grant a private, non-custom sourceDefinition to a given workspace """
        return PrivateSourceDefinition.parse_obj(
            self._api_request(
                'source_definitions/grant_definition',
                data=request
            ).json()
        )

    def revoke_grant_private_source_definition_for_workspace(
        self,
        request: GrantPrivateSourceDefinitionForWorkspaceRequest
    ) -> None:
        """ Revoke a grant to a private, non-custom sourceDefinition from a given workspace """
        self._api_request(
            'source_definitions/grant_definition',
            data=request
        ).json()

    def get_source_definition_specification(
        self,
        request: GetSourceDefinitionSpecificationRequest
    ) -> SourceDefinitionSpecification:
        """ Get specification for a SourceDefinition. """
        return SourceDefinitionSpecification.parse_obj(
            self._api_request(
                'source_definition_specifications/get',
                data=request
            ).json()
        )

    def create_source(
        self,
        request: CreateSourceRequest
    ) -> Source:
        """ Create a source """
        return Source.parse_obj(
            self._api_request(
                'sources/create',
                data=request
            ).json()
        )

    def update_source(
        self,
        request: UpdateSourceRequest
    ) -> Source:
        """ Update a source """
        return Source.parse_obj(
            self._api_request(
                'sources/update',
                data=request
            ).json()
        )

    def list_workspace_sources(
        self,
        request: ListWorkspaceSourcesRequest
    ) -> list[Source]:
        """ List sources for workspace. Does not return deleted sources. """
        return [
            Source.parse_obj(source)
            for source in self._api_request(
                'sources/list',
                data=request
            ).json()['sources']
        ]

    def get_source(
        self,
        request: GetSourceRequest
    ) -> Source:
        """ Get source """
        return Source.parse_obj(
            self._api_request(
                'sources/get',
                data=request
            ).json()
        )

    def search_source(
        self,
        request: SearchSourceRequest
    ) -> list[Source]:
        """ Search sources """
        return [
            Source.parse_obj(source)
            for source in self._api_request(
                'sources/search',
                data=request
            ).json()['sources']
        ]

    def clone_source(
        self,
        request: CloneSourceRequest
    ) -> Source:
        """ Clone source """
        return Source.parse_obj(
            self._api_request(
                'sources/clone',
                data=request
            ).json()
        )

    def delete_source(
        self,
        request: DeleteSourceRequest
    ) -> None:
        """ Delete a source """
        self._api_request(
            'sources/delete',
            data=request
        ).json()

    def check_source_connection(
        self,
        request: CheckSourceConnectionRequest
    ) -> CheckConnectionStatus:
        """ Check connection to the source """
        return CheckConnectionStatus.parse_obj(
            self._api_request(
                'sources/check_connection',
                data=request
            ).json()
        )

    def check_source_connection_for_update(
        self,
        request: CheckConnectionForUpdateRequest
    ) -> CheckConnectionStatus:
        """ Check connection for a proposed update to a source """
        return CheckConnectionStatus.parse_obj(
            self._api_request(
                'sources/check_connection_for_update',
                data=request
            ).json()
        )

    def discover_source_schema(
        self,
        request: DiscoverSourceSchemaRequest
    ) -> SourceDiscoverSchemaJob:
        """ Discover the schema catalog of the source """
        return SourceDiscoverSchemaJob.parse_obj(
            self._api_request(
                'sources/discover_schema',
                data=request
            ).json()
        )

    def create_destination_definition(
        self,
        request: CreateDestinationDefinitionRequest
    ) -> DestinationDefinition:
        """ Creates a destinationsDefinition """
        return DestinationDefinition.parse_obj(
            self._api_request(
                'destination_definitions/create',
                data=request
            ).json()
        )

    def update_destination_definition(
        self,
        request: UpdateDestinationDefinitionRequest
    ) -> DestinationDefinition:
        """ Update destinationDefinition """
        return DestinationDefinition.parse_obj(
            self._api_request(
                'destination_definitions/update',
                data=request
            ).json()
        )

    def list_destination_definition(self) -> list[DestinationDefinition]:
        """
        List all the destinationDefinitions the current
        Airbyte deployment is configured to use
        """
        return [
            DestinationDefinition.parse_obj(source)
            for source in self._api_request(
                'destination_definitions/list',
            ).json()['destinationDefinitions']
        ]

    def list_latest_destination_definition(self) -> list[DestinationDefinition]:
        """
        List the latest destinationDefinitions Airbyte supports.
        Guaranteed to retrieve the latest information on supported destinations.
        """
        return [
            DestinationDefinition.parse_obj(destination_definition)
            for destination_definition in self._api_request(
                'destination_definitions/list_latest',
            ).json()['destinationDefinitions']
        ]

    def get_destination_definition(
        self,
        request: GetDestinationDefinitionRequest
    ) -> DestinationDefinition:
        """ Get destinationDefinition """
        return DestinationDefinition.parse_obj(
            self._api_request(
                'destination_definitions/get',
                data=request
            ).json()
        )

    def delete_destination_definition(
        self,
        request: DeleteDestinationDefinitionRequest
    ) -> None:
        """ Delete a destination definition """
        self._api_request(
            'destination_definitions/delete',
            data=request
        )

    def list_private_destination_definition(
        self,
        request: ListPrivateDestinationDefinitionRequest
    ) -> list[DestinationDefinition]:
        """
        List all private, non-custom destinationDefinitions,
        and for each indicate whether the given workspace
        has a grant for using the definition
        """
        return [
            DestinationDefinition.parse_obj(destination_definition)
            for destination_definition in self._api_request(
                'destination_definitions/list_private',
                data=request
            ).json()['destinationDefinitions']
        ]

    def get_destination_definition_specification(
        self,
        request: GetDestinationDefinitionSpecificationRequest
    ) -> DestinationDefinitionSpecification:
        return DestinationDefinitionSpecification.parse_obj(
            self._api_request(
                'destination_definition_specifications/get',
                data=request
            ).json()
        )

    def create_destination(
        self, request: CreateDestinationRequest
    ) -> Destination:
        return Destination.parse_obj(
            self._api_request(
                'destinations/create',
                data=request
            ).json()
        )

    def update_destination(
        self, request: UpdateDestinationRequest
    ) -> Destination:
        return Destination.parse_obj(
            self._api_request(
                'destinations/update',
                data=request
            ).json()
        )

    def list_destinations(
        self,
        request: ListDestinationsRequest
    ) -> list[Destination]:
        return [
            Destination.parse_obj(destination)
            for destination in self._api_request(
                'destinations/list',
                data=request
            ).json()['destinations']
        ]

    def get_destination(
        self,
        request: GetDestinationRequest
    ) -> Destination:
        return Destination.parse_obj(
            self._api_request(
                'destinations/get',
                data=request
            ).json()
        )

    def search_destinations(
        self,
        request: SearchDestinationsRequest
    ) -> list[Destination]:
        return [
            Destination.parse_obj(destination)
            for destination in self._api_request(
                'destinations/search',
                data=request
            ).json()['destinations']
        ]

    def check_destination_connection(
        self,
        request: CheckDestinationConnectionRequest
    ) -> CheckConnectionStatus:
        return CheckConnectionStatus.parse_obj(
            self._api_request(
                'destinations/check_connection',
                data=request
            ).json()
        )

    def check_destination_connection_for_update(
        self,
        request: CheckDestinationConnectionForUpdateRequest
    ) -> CheckConnectionStatus:
        return CheckConnectionStatus.parse_obj(
            self._api_request(
                'destinations/check_connection_for_update',
                data=request
            ).json()
        )

    def delete_destination(
        self,
        request: DeleteDestinationRequest
    ) -> None:
        self._api_request(
            'destinations/delete',
            data=request
        )

    def clone_destination(
        self,
        request: CloneDestinationRequest
    ) -> Destination:
        return Destination.parse_obj(
            self._api_request(
                'destinations/clone',
                data=request
            ).json()
        )

    def create_connection(
        self,
        request: Connection
    ) -> Connection:
        return Connection.parse_obj(
            self._api_request(
                'connections/create',
                data=request
            ).json()
        )

    def update_connection(
        self,
        request: UpdateConnectionRequest
    ) -> Connection:
        return Connection.parse_obj(
            self._api_request(
                'connections/update',
                data=request
            ).json()
        )

    def list_connections(
        self,
        request: ConnectionsListRequest
    ) -> list[Connection]:
        return [
            Connection.parse_obj(connection)
            for connection in self._api_request(
                'connections/list',
                data=request
            ).json()['connections']
        ]

    def list_all_workspace_connections(
        self,
        request: ListAllConnectionRequest
    ) -> list[Connection]:
        """List connections for workspace, including deleted connections."""
        return [
            Connection.parse_obj(connection)
            for connection in self._api_request(
                'connections/list_all',
                data=request
            ).json()['connections']
        ]

    def get_connection(
        self,
        request: GetConnectionRequest
    ) -> Connection:
        return Connection.parse_obj(
            self._api_request(
                'connections/get',
                data=request
            ).json()
        )

    def get_connection_state(
        self,
        request: GetConnectionStateRequest
    ) -> ConnectionState:
        """ Fetch the current state for a connection. """
        return ConnectionState.parse_obj(
            self._api_request(
                'state/get',
                data=request
            ).json()
        )

    def create_or_update_connection_state(
        self,
        request: CreateOrUpdateConnectionStateRequest
    ) -> ConnectionState:
        """ Create or update the state for a connection. """
        return ConnectionState.parse_obj(
            self._api_request(
                'state/create_or_update',
                data=request
            ).json()
        )

    def search_connections(
        self,
        request: SearchConnectionsRequest
    ) -> list[Connection]:
        return [
            Connection.parse_obj(connection)
            for connection in self._api_request(
                'connections/search',
                data=request
            ).json()['connections']
        ]

    def delete_connection(
        self,
        request: DeleteConnectionRequest
    ) -> None:
        """ Delete a connection """
        self._api_request(
            'connections/delete',
            data=request
        )

    def sync_connection(
        self,
        request: SyncConnectionRequest
    ) -> DetailedJob:
        return DetailedJob.parse_obj(
            self._api_request(
                'connections/sync',
                data=request
            ).json()
        )

    def reset_connection(
        self,
        request: ResetConnectionRequest
    ) -> DetailedJob:
        return DetailedJob.parse_obj(
            self._api_request(
                'connections/reset',
                data=request
            ).json()
        )

    def get_connection_state_type(
        self,
        request: GetConnectionStateTypeRequest
    ) -> str:
        """ Fetch the current state type for a connection. """
        return self._api_request(
            'web_backend/state/get_type',
            data=request
        ).json()

    def get_job(self, request: GetJobRequest) -> DetailedJob:
        """ Get information about job """
        return DetailedJob.parse_obj(
            self._api_request(
                'jobs/get',
                data=request
            ).json()
        )

    def list_jobs(self, request: ListJobsRequest) -> list[DetailedJob]:
        return [
            DetailedJob.parse_obj(connection)
            for connection in self._api_request(
                'jobs/list',
                data=request
            ).json()['jobs']
        ]

    def get_light_job(self, request: GetJobRequest) -> Job:
        return Job.parse_obj(
            self._api_request(
                'jobs/get_light',
                data=request
            ).json()
        )

    def cancel_job(self, request: CancelJobRequest) -> DetailedJob:
        return DetailedJob.parse_obj(
            self._api_request(
                'jobs/cancel',
                data=request
            ).json()
        )

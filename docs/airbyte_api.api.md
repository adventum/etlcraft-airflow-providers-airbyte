<!-- markdownlint-disable -->

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `airbyte_api.api`






---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AirbyteApi`




<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    airbyte_url_base: str = 'http://localhost:8000/api/v1',
    auth: Optional[HTTPBasicAuth] = None
)
```








---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L758"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `cancel_job`

```python
cancel_job(request: CancelJobRequest) → DetailedJob
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L554"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `check_destination_connection`

```python
check_destination_connection(
    request: CheckDestinationConnectionRequest
) → CheckConnectionStatus
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L565"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `check_destination_connection_for_update`

```python
check_destination_connection_for_update(
    request: CheckDestinationConnectionForUpdateRequest
) → CheckConnectionStatus
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L365"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `check_source_connection`

```python
check_source_connection(
    request: CheckSourceConnectionRequest
) → CheckConnectionStatus
```

Check connection to the source  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L377"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `check_source_connection_for_update`

```python
check_source_connection_for_update(
    request: CheckConnectionForUpdateRequest
) → CheckConnectionStatus
```

Check connection for a proposed update to a source  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L585"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clone_destination`

```python
clone_destination(request: CloneDestinationRequest) → Destination
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L343"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clone_source`

```python
clone_source(request: CloneSourceRequest) → Source
```

Clone source  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L596"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_connection`

```python
create_connection(request: Connection) → Connection
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L202"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_custom_source_definition_for_workspace`

```python
create_custom_source_definition_for_workspace(
    request: CreateCustomSourceDefinitionForWorkspaceRequest
) → SourceDefinition
```

Creates a custom sourceDefinition for the given workspace  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L499"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_destination`

```python
create_destination(request: CreateDestinationRequest) → Destination
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L401"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_destination_definition`

```python
create_destination_definition(
    request: CreateDestinationDefinitionRequest
) → DestinationDefinition
```

Creates a destinationsDefinition  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L666"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_or_update_connection_state`

```python
create_or_update_connection_state(
    request: CreateOrUpdateConnectionStateRequest
) → ConnectionState
```

Create or update the state for a connection.  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L281"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_source`

```python
create_source(request: CreateSourceRequest) → Source
```

Create a source  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L96"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_source_definition`

```python
create_source_definition(
    request: CreateSourceDefinitionRequest
) → SourceDefinition
```

Creates a sourceDefinition  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L690"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `delete_connection`

```python
delete_connection(request: DeleteConnectionRequest) → None
```

Delete a connection  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L238"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `delete_custom_source_definition_for_workspace`

```python
delete_custom_source_definition_for_workspace(
    request: DeleteCustomSourceDefinitionForWorkspaceRequest
) → None
```

Delete a custom source definition for the given workspace  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L576"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `delete_destination`

```python
delete_destination(request: DeleteDestinationRequest) → None
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L461"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `delete_destination_definition`

```python
delete_destination_definition(
    request: DeleteDestinationDefinitionRequest
) → None
```

Delete a destination definition  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L355"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `delete_source`

```python
delete_source(request: DeleteSourceRequest) → None
```

Delete a source  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L158"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `delete_source_definition`

```python
delete_source_definition(
    request: DeleteSourceDefinitionRequest
) → SourceDefinition
```

Delete a source definition 

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L389"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `discover_source_schema`

```python
discover_source_schema(
    request: DiscoverSourceSchemaRequest
) → SourceDiscoverSchemaJob
```

Discover the schema catalog of the source  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L643"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_connection`

```python
get_connection(request: GetConnectionRequest) → Connection
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L654"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_connection_state`

```python
get_connection_state(request: GetConnectionStateRequest) → ConnectionState
```

Fetch the current state for a connection.  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L722"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_connection_state_type`

```python
get_connection_state_type(request: GetConnectionStateTypeRequest) → str
```

Fetch the current state type for a connection.  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L531"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_destination`

```python
get_destination(request: GetDestinationRequest) → Destination
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L449"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_destination_definition`

```python
get_destination_definition(
    request: GetDestinationDefinitionRequest
) → DestinationDefinition
```

Get destinationDefinition  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L488"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_destination_definition_specification`

```python
get_destination_definition_specification(
    request: GetDestinationDefinitionSpecificationRequest
) → DestinationDefinitionSpecification
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L732"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_job`

```python
get_job(request: GetJobRequest) → DetailedJob
```

Get information about job  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L750"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_light_job`

```python
get_light_job(request: GetJobRequest) → Job
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L318"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_source`

```python
get_source(request: GetSourceRequest) → Source
```

Get source  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L146"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_source_definition`

```python
get_source_definition(request: GetSourceDefinitionRequest) → SourceDefinition
```

Get source definition  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L214"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_source_definition_for_workspace`

```python
get_source_definition_for_workspace(
    request: GetSourceDefinitionForWorkspaceRequest
) → SourceDefinition
```

Get a sourceDefinition that is configured for the given workspace  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L269"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_source_definition_specification`

```python
get_source_definition_specification(
    request: GetSourceDefinitionSpecificationRequest
) → SourceDefinitionSpecification
```

Get specification for a SourceDefinition.  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L247"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `grant_private_source_definition_for_workspace`

```python
grant_private_source_definition_for_workspace(
    request: GrantPrivateSourceDefinitionForWorkspaceRequest
) → PrivateSourceDefinition
```

Grant a private, non-custom sourceDefinition to a given workspace  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L79"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `health_check`

```python
health_check() → bool
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L630"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_all_workspace_connections`

```python
list_all_workspace_connections(
    request: ListAllConnectionRequest
) → list[Connection]
```

List connections for workspace, including deleted connections. 

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L618"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_connections`

```python
list_connections(request: ConnectionsListRequest) → list[Connection]
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L425"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_destination_definition`

```python
list_destination_definition() → list[DestinationDefinition]
```

List all the destinationDefinitions the current Airbyte deployment is configured to use 

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L519"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_destinations`

```python
list_destinations(request: ListDestinationsRequest) → list[Destination]
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L741"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_jobs`

```python
list_jobs(request: ListJobsRequest) → list[DetailedJob]
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L437"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_latest_destination_definition`

```python
list_latest_destination_definition() → list[DestinationDefinition]
```

List the latest destinationDefinitions Airbyte supports. Guaranteed to retrieve the latest information on supported destinations. 

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_latest_source_definitions`

```python
list_latest_source_definitions() → list[SourceDefinition]
```

List the latest sourceDefinitions Airbyte supports. Guaranteed to retrieve the latest information on supported sources. 

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L471"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_private_destination_definition`

```python
list_private_destination_definition(
    request: ListPrivateDestinationDefinitionRequest
) → list[DestinationDefinition]
```

List all private, non-custom destinationDefinitions, and for each indicate whether the given workspace has a grant for using the definition 

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L172"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_private_source_definitions`

```python
list_private_source_definitions(
    request: ListPrivateSourceDefinitionRequest
) → list[PrivateSourceDefinition]
```

List all private, non-custom sourceDefinitions, and for each indicate whether the given workspace has a grant for using the definition 

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L123"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_source_definitions`

```python
list_source_definitions() → list[SourceDefinition]
```

List all the sourceDefinitions the current Airbyte deployment is configured to use 

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L189"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_source_definitions_for_workspace`

```python
list_source_definitions_for_workspace(
    request: ListSourceDefinitionForWorkspaceRequest
) → list[SourceDefinition]
```

List all the sourceDefinitions the given workspace is configured to use  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L305"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_workspace_sources`

```python
list_workspace_sources(request: ListWorkspaceSourcesRequest) → list[Source]
```

List sources for workspace. Does not return deleted sources.  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_workspaces`

```python
list_workspaces() → list[Workspace]
```

List all workspaces registered in the current Airbyte deployment  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L711"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `reset_connection`

```python
reset_connection(request: ResetConnectionRequest) → DetailedJob
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L259"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `revoke_grant_private_source_definition_for_workspace`

```python
revoke_grant_private_source_definition_for_workspace(
    request: GrantPrivateSourceDefinitionForWorkspaceRequest
) → None
```

Revoke a grant to a private, non-custom sourceDefinition from a given workspace  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L678"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `search_connections`

```python
search_connections(request: SearchConnectionsRequest) → list[Connection]
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L542"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `search_destinations`

```python
search_destinations(request: SearchDestinationsRequest) → list[Destination]
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L330"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `search_source`

```python
search_source(request: SearchSourceRequest) → list[Source]
```

Search sources  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L700"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `sync_connection`

```python
sync_connection(request: SyncConnectionRequest) → DetailedJob
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L607"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_connection`

```python
update_connection(request: UpdateConnectionRequest) → Connection
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L226"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_custom_source_definition_for_workspace`

```python
update_custom_source_definition_for_workspace(
    request: UpdateCustomSourceDefinitionForWorkspaceRequest
) → SourceDefinition
```

Update a custom sourceDefinition for the given workspace  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L509"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_destination`

```python
update_destination(request: UpdateDestinationRequest) → Destination
```





---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L413"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_destination_definition`

```python
update_destination_definition(
    request: UpdateDestinationDefinitionRequest
) → DestinationDefinition
```

Update destinationDefinition  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L293"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_source`

```python
update_source(request: UpdateSourceRequest) → Source
```

Update a source  

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_api/api.py#L108"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_source_definition`

```python
update_source_definition(
    request: UpdateSourceDefinitionRequest
) → SourceDefinition
```

Update the SourceDefinition. Currently, the only allowed attribute to  update is the default docker image version.  




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

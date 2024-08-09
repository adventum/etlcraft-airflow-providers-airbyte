from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class AuthFlowType(str, Enum):
    oauth2_0: str = "oauth2.0"
    oauth1_0: str = "oauth1.0"


class DestinationSyncMode(str, Enum):
    append: str = "append"
    overwrite: str = "overwrite"
    append_dedup: str = "append_dedup"


class SyncMode(str, Enum):
    full_refresh: str = "full_refresh"
    incremental: str = "incremental"


class _AirbyteStream(BaseModel, extra="allow"):

    name: str
    json_schema: Dict[str, Any]
    supported_sync_modes: Optional[List[SyncMode]] = Field(default=None)
    source_defined_cursor: Optional[bool] = Field(default=None)
    default_cursor_field: Optional[List[str]] = Field(default=None)
    source_defined_primary_key: Optional[List[List[str]]] = Field(default=None)
    namespace: Optional[str] = Field(default=None)


class ConfiguredAirbyteStream(BaseModel, extra="allow"):

    stream: _AirbyteStream
    sync_mode: SyncMode
    cursor_field: Optional[List[str]] = Field(default=None)
    destination_sync_mode: DestinationSyncMode
    primary_key: Optional[List[List[str]]] = Field(default=None)


class ConfiguredAirbyteCatalog(BaseModel, extra="allow"):
    streams: List[ConfiguredAirbyteStream]


class AuthType(str, Enum):
    oauth2_0: str = "oauth2.0"


class OAuth2Specification(BaseModel, extra="allow"):
    rootObject: Optional[List[Union[str, int]]] = Field(default=None)
    oauthFlowInitParameters: Optional[List[List[str]]] = Field(default=None)
    oauthFlowOutputParameters: Optional[List[List[str]]] = Field(default=None)


class OAuthConfigSpecification(BaseModel, extra="allow"):

    oauth_user_input_from_connector_config_specification: Optional[Dict[str, Any]] = (
        Field(default=None)
    )
    complete_oauth_output_specification: Optional[Dict[str, Any]] = Field(default=None)
    complete_oauth_server_input_specification: Optional[Dict[str, Any]] = Field(
        default=None
    )
    complete_oauth_server_output_specification: Optional[Dict[str, Any]] = Field(
        default=None
    )


class AuthSpecification(BaseModel):
    auth_type: Optional[AuthType] = Field(default=None)
    oauth2Specification: Optional[OAuth2Specification] = Field(default=None)


class AdvancedAuth(BaseModel):
    auth_flow_type: Optional[AuthFlowType] = Field(default=None)
    predicate_key: Optional[List[str]] = Field(default=None)
    predicate_value: Optional[str] = Field(default=None)
    oauth_config_specification: Optional[OAuthConfigSpecification] = Field(default=None)


class StreamDescriptor(BaseModel, extra="allow"):

    name: str
    namespace: Optional[str] = Field(default=None)


class AirbyteStateBlob(BaseModel, extra="allow"): ...


class AirbyteStreamState(BaseModel, extra="allow"):
    stream_descriptor: StreamDescriptor
    stream_state: Optional[AirbyteStateBlob] = Field(default=None)


class AirbyteCatalog(BaseModel, extra="allow"):
    streams: List[_AirbyteStream]


class AirbyteGlobalState(BaseModel, extra="allow"):
    shared_state: Optional[AirbyteStateBlob] = Field(default=None)
    stream_states: List[AirbyteStreamState]


class JobStatus(str, Enum):
    RUNNING: str = "running"
    SUCCEEDED: str = "succeeded"
    CANCELLED: str = "cancelled"
    PENDING: str = "pending"
    FAILED: str = "failed"
    ERROR: str = "error"
    INCOMPLETE: str = "incomplete"


def to_camel(string: str) -> str:
    return "".join(
        word.capitalize() if word_n > 0 else word
        for word_n, word in enumerate(string.split("_"))
    )


class ApiBaseModel(BaseModel, extra="allow"):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        allow_population_by_alias = True
        populate_by_name = True


class AirbyteStream(ApiBaseModel):
    name: str
    json_schema: Dict[str, Any]
    supported_sync_modes: Optional[List[SyncMode]] = Field(default=None)
    source_defined_cursor: Optional[bool] = Field(default=None)
    default_cursor_field: Optional[List[str]] = Field(default=None)
    source_defined_primary_key: Optional[List[List[str]]] = Field(default=None)
    namespace: Optional[str] = Field(default=None)


class GetJobRequest(ApiBaseModel):
    id: int


class Pagination(ApiBaseModel):
    page_size: int
    row_offset: int


class ListJobsRequest(ApiBaseModel):
    config_types: List[str]
    config_id: str
    including_job_id: int
    pagination: Pagination


class ResourceRequirements(ApiBaseModel):
    cpu_request: Optional[str] = Field(default=None)
    cpu_limit: Optional[str] = Field(default=None)
    memory_request: Optional[str] = Field(default=None)
    memory_limit: Optional[str] = Field(default=None)

    class Config:
        def alias_generator(field_name):
            return field_name


class JobSpecificResourceRequirements(ApiBaseModel):
    job_type: str
    resource_requirements: ResourceRequirements


class DefinitionResourceRequirements(ApiBaseModel):
    default: ResourceRequirements
    job_specific: Optional[List[JobSpecificResourceRequirements]] = Field(default=None)


class CreateSourceDefinitionRequest(ApiBaseModel):
    name: str
    docker_repository: str
    docker_image_tag: str
    documentation_url: str
    icon: Optional[str] = Field(default=None)
    resource_requirements: Optional[DefinitionResourceRequirements] = Field(
        default=None
    )


class UpdateSourceDefinitionRequest(ApiBaseModel):
    source_definition_id: str
    docker_image_tag: str


class GetSourceDefinitionRequest(ApiBaseModel):
    source_definition_id: str


class DeleteSourceDefinitionRequest(ApiBaseModel):
    source_definition_id: str


class ListPrivateSourceDefinitionRequest(ApiBaseModel):
    workspace_id: str


class ListSourceDefinitionForWorkspaceRequest(ApiBaseModel):
    workspace_id: str


class CreateCustomSourceDefinitionForWorkspaceRequest(ApiBaseModel):
    workspace_id: str
    source_definition: CreateSourceDefinitionRequest


class GetSourceDefinitionForWorkspaceRequest(ApiBaseModel):
    workspace_id: str
    source_definition_id: str


class UpdateCustomSourceDefinitionForWorkspaceRequest(ApiBaseModel):
    workspace_id: str
    source_definition: UpdateSourceDefinitionRequest


class DeleteCustomSourceDefinitionForWorkspaceRequest(ApiBaseModel):
    workspace_id: str
    source_definition_id: UpdateSourceDefinitionRequest


class GrantPrivateSourceDefinitionForWorkspaceRequest(ApiBaseModel):
    source_definition_id: str
    workspace_id: str


class SourceDefinition(ApiBaseModel):
    source_definition_id: str
    name: str
    docker_repository: str
    docker_image_tag: str
    documentation_url: Optional[str] = Field(default=None)
    icon: Optional[str] = Field(default=None)
    protocol_version: Optional[str] = Field(default=None)
    release_stage: Optional[str] = Field(default=None)
    release_date: Optional[str] = Field(default=None)
    source_type: Optional[str] = Field(default=None)
    resource_requirements: Optional[DefinitionResourceRequirements] = Field(
        default=None
    )


class PrivateSourceDefinition(ApiBaseModel):
    source_definition: SourceDefinition
    granted: bool


class Logs(ApiBaseModel):
    log_lines: List[str]


class JobInfo(ApiBaseModel):
    id: str
    config_type: str
    config_if: Optional[str] = Field(default=None)
    created_at: int
    ended_at: int
    succeeded: Optional[bool] = Field(default=None)
    logs: Logs


class SourceDefinitionSpecification(ApiBaseModel):
    source_definition_id: str
    documentation_uri: Optional[str] = Field(default=None)
    connection_specification: Dict[str, Any]
    auth_specification: Optional[AuthSpecification] = Field(default=None)
    advanced_auth: Optional[AdvancedAuth] = Field(default=None)
    job_info: JobInfo


class DestinationDefinitionSpecification(ApiBaseModel):
    destination_definition_id: str
    documentation_uri: str
    connection_specification: Dict[str, Any]
    auth_specification: AuthSpecification
    advanced_auth: AdvancedAuth
    job_info: JobInfo


class CreateSourceRequest(ApiBaseModel):
    source_definition_id: str
    connection_configuration: Dict[str, Any]
    workspace_id: str
    name: str


class UpdateSourceRequest(ApiBaseModel):
    source_id: str
    connection_configuration: Optional[Dict[str, Any]] = Field(default=None)
    name: Optional[str] = Field(default=None)


class CheckSourceConnectionRequest(ApiBaseModel):
    source_id: str


class CheckConnectionForUpdateRequest(ApiBaseModel):
    source_id: str
    connection_configuration: Dict[str, Any]
    name: str


class ListWorkspaceSourcesRequest(ApiBaseModel):
    workspace_id: str


class GetSourceRequest(ApiBaseModel):
    source_id: str


class GetSourceDefinitionSpecificationRequest(ApiBaseModel):
    source_definition_id: str
    workspace_id: str


class Source(ApiBaseModel):
    source_definition_id: str
    source_id: str
    workspace_id: str
    connection_configuration: Dict[str, Any]
    name: str
    source_name: str


class SourceConfiguration(ApiBaseModel):
    connection_configuration: Dict[str, Any]
    name: str


class DeleteSourceRequest(ApiBaseModel):
    source_id: str


class CloneSourceRequest(ApiBaseModel):
    source_clone_id: str
    source_configuration: SourceConfiguration


class SearchSourceRequest(ApiBaseModel):
    source_definitionId: Optional[str] = Field(default=None)
    source_id: Optional[str] = Field(default=None)
    workspace_id: Optional[str] = Field(default=None)
    connection_configuration: Optional[Dict[str, Any]] = Field(default=None)
    name: Optional[str] = Field(default=None)
    source_name: Optional[str] = Field(default=None)


class CheckConnectionStatus(ApiBaseModel):
    status: str
    message: Optional[str] = Field(default=None)
    job_info: JobInfo


class CreateDestinationDefinitionRequest(ApiBaseModel):
    name: str
    docker_repository: str
    docker_image_tag: str
    documentation_url: str
    icon: str = None
    resource_requirements: DefinitionResourceRequirements = None


class UpdateDestinationDefinitionRequest(ApiBaseModel):
    destination_definition_id: str
    docker_image_tag: str
    resource_requirements: DefinitionResourceRequirements = None


class DiscoverSourceSchemaRequest(ApiBaseModel):
    source_id: str
    disable_cache: bool


class DeleteConnectionRequest(ApiBaseModel):
    connection_id: str


class SourceDiscoverSchemaJob(ApiBaseModel):
    catalog: AirbyteCatalog
    job_info: JobInfo
    catalog_id: str


class DestinationDefinition(ApiBaseModel):
    destination_definition_id: str
    name: str
    docker_repository: str
    docker_image_tag: str
    documentation_uri: str
    icon: str
    protocol_version: str
    release_stage: str
    release_date: str
    source_type: str
    resource_requirements: DefinitionResourceRequirements


class GetDestinationDefinitionRequest(ApiBaseModel):
    destination_definition_id: str


class DeleteDestinationDefinitionRequest(ApiBaseModel):
    destination_definition_id: str


class ListPrivateDestinationDefinitionRequest(ApiBaseModel):
    workspace_id: str


class Destination(ApiBaseModel):
    destination_definition_id: str
    destination_id: str
    workspace_id: str
    connection_configuration: Dict[str, Any]
    name: str
    destination_name: str


class CreateDestinationRequest(ApiBaseModel):
    workspace_id: str
    name: str
    destination_definition_id: str
    connection_configuration: Dict[str, Any]


class UpdateDestinationRequest(ApiBaseModel):
    destination_id: str
    connection_configuration: Dict[str, Any]
    name: str


class ListDestinationsRequest(ApiBaseModel):
    workspace_id: str


class GetDestinationRequest(ApiBaseModel):
    destination_id: str


class SearchDestinationsRequest(ApiBaseModel):
    destination_definition_id: str
    destination_id: str
    workspace_id: str
    connection_configuration: Dict[str, Any]
    name: str
    destination_name: str


class CheckDestinationConnectionRequest(ApiBaseModel):
    destination_id: str


class CheckDestinationConnectionForUpdateRequest(ApiBaseModel):
    destination_id: str
    connection_configuration: Dict[str, Any]
    name: str


class DeleteDestinationRequest(ApiBaseModel):
    destination_id: str


class DestinationConfiguration(ApiBaseModel):
    connection_configuration: Dict[str, Any]
    name: str


class CreateConnectionRequest(ApiBaseModel):
    name: str
    namespace_definition: str
    namespace_format: str
    prefix: str
    source_id: str
    destination_id: str
    operations_ids: List[str]
    sync_catalog: ConfiguredAirbyteCatalog


class CloneDestinationRequest(ApiBaseModel):
    destination_clone_id: Optional[str] = Field(default=None)
    destination_configuration: Optional[DestinationConfiguration] = Field(default=None)


class GetDestinationDefinitionSpecificationRequest(ApiBaseModel):
    destination_definition_id: Optional[str] = Field(default=None)
    workspace_id: Optional[str] = Field(default=None)


class ConnectionSchedule(ApiBaseModel):
    time_unit: Optional[str] = Field(default=None)
    units: Optional[int] = Field(default=None)


class ConnectionScheduleCron(ApiBaseModel):
    cron_expression: Optional[str] = Field(default=None)
    cron_timezone: Optional[str] = Field(default=None)


class ConnectionScheduleData(ApiBaseModel):
    basic_schedule: Optional[ConnectionSchedule] = Field(default=None)
    cron: Optional[ConnectionScheduleCron] = Field(default=None)


class ConnectionSyncCatalogStreamConfig(ApiBaseModel):
    sync_mode: Optional[SyncMode] = Field(default=None)
    cursor_field: List[str]
    destination_sync_mode: Optional[DestinationSyncMode] = Field(default=None)
    primary_key: Optional[List[List[str]]] = Field(default=None)
    alias_name: Optional[str] = Field(default=None)
    selected: Optional[bool] = Field(default=None)


class ConnectionSyncCatalogStream(ApiBaseModel):
    stream: Optional[AirbyteStream] = Field(default=None)
    config: Optional[ConnectionSyncCatalogStreamConfig] = Field(default=None)


class ConnectionSyncCatalog(ApiBaseModel):
    streams: List[ConnectionSyncCatalogStream]


class UpdateConnectionRequest(ApiBaseModel):
    connection_id: str
    namespace_definition: Optional[str] = Field(default=None)
    namespace_format: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    prefix: Optional[str] = Field(default=None)
    operation_ids: Optional[List[str]] = Field(default=None)
    sync_catalog: ConnectionSyncCatalog
    schedule: Optional[ConnectionSchedule] = Field(default=None)
    schedule_type: Optional[str] = Field(default=None)
    schedule_data: Optional[ConnectionScheduleData] = Field(default=None)
    status: str
    resource_requirements: Optional[ResourceRequirements] = Field(default=None)
    source_catalog_id: Optional[str] = Field(default=None)


class SlackConfiguration(ApiBaseModel):
    webhook: str


class Notification(ApiBaseModel):
    notificationType: Optional[str] = Field(default=None)
    send_on_success: Optional[bool] = Field(default=None)
    send_on_failure: Optional[bool] = Field(default=None)
    slack_configuration: Optional[SlackConfiguration] = Field(default=None)
    customerio_configuration: Optional[Dict[str, Any]] = Field(default=None)


class Workspace(ApiBaseModel):
    workspace_id: Optional[str] = Field(default=None)
    customer_id: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    slug: Optional[str] = Field(default=None)
    initial_setup_complete: Optional[bool] = Field(default=None)
    display_setup_wizard: Optional[bool] = Field(default=None)
    anonymous_data_collection: Optional[bool] = Field(default=None)
    news: Optional[bool] = Field(default=None)
    security_updates: Optional[bool] = Field(default=None)
    notifications: List[Notification]
    first_completed_sync: Optional[bool] = Field(default=None)
    feedback_done: Optional[bool] = Field(default=None)


class ConnectionsListRequest(ApiBaseModel):
    workspace_id: str


class GetConnectionRequest(ApiBaseModel):
    connection_id: str


class GetConnectionStateRequest(ApiBaseModel):
    connection_id: str


class ListAllConnectionRequest(ApiBaseModel):
    workspace_id: str


class Connection(ApiBaseModel):
    """Describes Airbyte connection between source and destination"""

    connection_id: str
    name: Optional[str] = Field(default=None)
    namespace_definition: Optional[str] = Field(default=None)
    namespace_format: Optional[str] = Field(default=None)
    prefix: Optional[str] = Field(default=None)
    source_id: str
    destination_id: str
    operation_ids: List[str]
    sync_catalog: ConnectionSyncCatalog = Field(default=None)
    schedule: Optional[ConnectionSchedule] = Field(default=None)
    schedule_type: Optional[str] = Field(default=None)
    schedule_data: Optional[ConnectionScheduleData] = Field(default=None)
    status: Optional[str] = Field(default=None)
    resource_requirements: Optional[ResourceRequirements] = Field(default=None)
    source_catalog_id: Optional[str] = Field(default=None)


class SearchConnectionsRequest(ApiBaseModel):
    connection_id: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    namespace_definition: Optional[str] = Field(default=None)
    namespace_format: Optional[str] = Field(default=None)
    prefix: Optional[str] = Field(default=None)
    source_id: Optional[str] = Field(default=None)
    destination_id: Optional[str] = Field(default=None)
    schedule: Optional[ConnectionSchedule] = Field(default=None)
    schedule_type: Optional[str] = Field(default=None)
    schedule_data: Optional[ConnectionScheduleData] = Field(default=None)
    status: Optional[str] = Field(default=None)
    source: Optional[Source] = Field(default=None)
    destination: Optional[Destination] = Field(default=None)


class HealthCheckStatus(ApiBaseModel):
    available: bool


class ConnectionState(ApiBaseModel):
    state_type: str
    connection_id: str
    state: Dict[str, Any]
    stream_state: List[AirbyteStreamState]
    global_state: AirbyteGlobalState


class SyncConnectionRequest(ApiBaseModel):
    connection_id: str


class GetConnectionStateTypeRequest(ApiBaseModel):
    connection_id: str


class ResetConnectionRequest(ApiBaseModel):
    connection_id: str


class CreateOrUpdateConnectionStateRequest(ApiBaseModel):
    connection_id: str
    connection_state: ConnectionState


class JobDefinitionResetConfig(ApiBaseModel):
    streams_to_reset: List[StreamDescriptor]


class JobDefinition(ApiBaseModel):
    id: int
    config_type: str
    config_id: str
    created_at: int
    updated_at: int
    status: JobStatus
    reset_config: Optional[JobDefinitionResetConfig] = Field(default=None)


class StreamStat(ApiBaseModel):
    records_emitted: int
    bytes_emitted: int
    state_messages_emitted: int
    records_committed: int


class StreamStatsDefinition(ApiBaseModel):
    stream_name: str
    stats: StreamStat


class JobFailure(ApiBaseModel):
    failure_origin: str
    failure_type: str
    external_message: str
    internal_message: str
    stack_trace: str
    retryable: bool
    timestamp: int


class JobFailureSummary(ApiBaseModel):
    failures: List[JobFailure]
    partial_success: bool


class JobAttemptDefinition(ApiBaseModel):
    id: int
    status: str
    created_at: int
    updated_at: int
    ended_at: Optional[int] = Field(default=None)
    bytes_synced: Optional[str] = Field(default=None)
    records_synced: Optional[str] = Field(default=None)
    total_stats: Optional[StreamStat] = Field(default=None)
    stream_stats: Optional[List[StreamStatsDefinition]] = Field(default=None)
    failure_summary: Optional[JobFailureSummary] = Field(default=None)


class JobAttemptLogs(ApiBaseModel):
    log_lines: List[str]


class JobAttempt(ApiBaseModel):
    attempt: JobAttemptDefinition
    logs: JobAttemptLogs


class DetailedJob(ApiBaseModel):
    job: JobDefinition
    attempts: List[JobAttempt]


class Job(ApiBaseModel):
    job: JobDefinition


class CancelJobRequest(ApiBaseModel):
    id: int

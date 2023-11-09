from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Extra


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


class _AirbyteStream(BaseModel):
    class Config:
        extra = Extra.allow

    name: str
    json_schema: Dict[str, Any]
    supported_sync_modes: Optional[List[SyncMode]]
    source_defined_cursor: Optional[bool]
    default_cursor_field: Optional[List[str]]
    source_defined_primary_key: Optional[List[List[str]]]
    namespace: Optional[str]


class ConfiguredAirbyteStream(BaseModel):
    class Config:
        extra = Extra.allow

    stream: _AirbyteStream
    sync_mode: SyncMode
    cursor_field: Optional[List[str]]
    destination_sync_mode: DestinationSyncMode
    primary_key: Optional[List[List[str]]]


class ConfiguredAirbyteCatalog(BaseModel):
    class Config:
        extra = Extra.allow

    streams: List[ConfiguredAirbyteStream]


class AuthType(str, Enum):
    oauth2_0: str = "oauth2.0"


class OAuth2Specification(BaseModel):
    class Config:
        extra = Extra.allow

    rootObject: Optional[List[Union[str, int]]]
    oauthFlowInitParameters: Optional[List[List[str]]]
    oauthFlowOutputParameters: Optional[List[List[str]]]


class OAuthConfigSpecification(BaseModel):
    class Config:
        extra = Extra.allow

    oauth_user_input_from_connector_config_specification: Optional[Dict[str, Any]]
    complete_oauth_output_specification: Optional[Dict[str, Any]]
    complete_oauth_server_input_specification: Optional[Dict[str, Any]]
    complete_oauth_server_output_specification: Optional[Dict[str, Any]]


class AuthSpecification(BaseModel):
    auth_type: Optional[AuthType]
    oauth2Specification: Optional[OAuth2Specification]


class AdvancedAuth(BaseModel):
    auth_flow_type: Optional[AuthFlowType]
    predicate_key: Optional[List[str]]
    predicate_value: Optional[str]
    oauth_config_specification: Optional[OAuthConfigSpecification]


class StreamDescriptor(BaseModel):
    class Config:
        extra = Extra.allow

    name: str
    namespace: Optional[str] = None


class AirbyteStateBlob(BaseModel):
    pass

    class Config:
        extra = Extra.allow


class AirbyteStreamState(BaseModel):
    class Config:
        extra = Extra.allow

    stream_descriptor: StreamDescriptor
    stream_state: Optional[AirbyteStateBlob] = None


class AirbyteCatalog(BaseModel):
    class Config:
        extra = Extra.allow

    streams: List[_AirbyteStream]


class AirbyteGlobalState(BaseModel):
    class Config:
        extra = Extra.allow

    shared_state: Optional[AirbyteStateBlob] = None
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
        word.capitalize() if word_n > 0 else word for word_n, word in enumerate(string.split("_"))
    )


class ApiBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        allow_population_by_field_name=True,
        allow_population_by_alias=True,
        extra=Extra.allow,
    )


class AirbyteStream(ApiBaseModel):
    name: str
    json_schema: Dict[str, Any]
    supported_sync_modes: Optional[List[SyncMode]]
    source_defined_cursor: Optional[bool]
    default_cursor_field: Optional[List[str]]
    source_defined_primary_key: Optional[List[List[str]]]
    namespace: Optional[str]


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
    cpu_request: Optional[str]
    cpu_limit: Optional[str]
    memory_request: Optional[str]
    memory_limit: Optional[str]

    class Config:
        def alias_generator(field_name):
            return field_name


class JobSpecificResourceRequirements(ApiBaseModel):
    job_type: str
    resource_requirements: ResourceRequirements


class DefinitionResourceRequirements(ApiBaseModel):
    default: ResourceRequirements
    job_specific: Optional[List[JobSpecificResourceRequirements]]


class CreateSourceDefinitionRequest(ApiBaseModel):
    name: str
    docker_repository: str
    docker_image_tag: str
    documentation_url: str
    icon: Optional[str]
    resource_requirements: Optional[DefinitionResourceRequirements]


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
    documentation_url: Optional[str]
    icon: Optional[str]
    protocol_version: Optional[str]
    release_stage: Optional[str]
    release_date: Optional[str]
    source_type: Optional[str]
    resource_requirements: Optional[DefinitionResourceRequirements]


class PrivateSourceDefinition(ApiBaseModel):
    source_definition: SourceDefinition
    granted: bool


class Logs(ApiBaseModel):
    log_lines: List[str]


class JobInfo(ApiBaseModel):
    id: str
    config_type: str
    config_if: Optional[str]
    created_at: int
    ended_at: int
    succeeded: Optional[bool]
    logs: Logs


class SourceDefinitionSpecification(ApiBaseModel):
    source_definition_id: str
    documentation_uri: Optional[str]
    connection_specification: Dict[str, Any]
    auth_specification: Optional[AuthSpecification]
    advanced_auth: Optional[AdvancedAuth]
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
    connection_configuration: Optional[Dict[str, Any]]
    name: Optional[str]


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
    source_definitionId: Optional[str]
    source_id: Optional[str]
    workspace_id: Optional[str]
    connection_configuration: Optional[Dict[str, Any]]
    name: Optional[str]
    source_name: Optional[str]


class CheckConnectionStatus(ApiBaseModel):
    status: str
    message: Optional[str]
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
    workspase_id: str
    connection_configuration: Dict[str, Any]
    name: str
    destination_name: str


class CreateDestinationRequest(ApiBaseModel):
    workspase_id: str
    name: str
    destination_definition_id: str
    connection_configuration: Dict[str, Any]


class UpdateDestinationRequest(ApiBaseModel):
    destination_id: str
    connection_configuration: Dict[str, Any]
    name: str


class ListDestinationsRequest(ApiBaseModel):
    worlspace_id: str


class GetDestinationRequest(ApiBaseModel):
    destination_id: str


class SearchDestinationsRequest(ApiBaseModel):
    destination_definition_id: str
    destination_id: str
    workspase_id: str
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
    destination_clone_id: Optional[str]
    destination_configuration: Optional[DestinationConfiguration]


class GetDestinationDefinitionSpecificationRequest(ApiBaseModel):
    destination_definition_id: Optional[str]
    workspace_id: Optional[str]


class ConnectionSchedule(ApiBaseModel):
    time_unit: Optional[str]
    units: Optional[int]


class ConnectionScheduleCron(ApiBaseModel):
    cron_expression: Optional[str]
    cron_timezone: Optional[str]


class ConnectionScheduleData(ApiBaseModel):
    basic_schedule: Optional[ConnectionSchedule]
    cron: Optional[ConnectionScheduleCron]


class ConnectionSyncCatalogStreamConfig(ApiBaseModel):
    sync_mode: Optional[SyncMode]
    cursor_field: List[str]
    destination_sync_mode: Optional[DestinationSyncMode]
    primary_key: Optional[List[List[str]]]
    alias_name: Optional[str]
    selected: Optional[bool]


class ConnectionSyncCatalogStream(ApiBaseModel):
    stream: Optional[AirbyteStream]
    config: Optional[ConnectionSyncCatalogStreamConfig]


class ConnectionSyncCatalog(ApiBaseModel):
    streams: List[ConnectionSyncCatalogStream]


class UpdateConnectionRequest(ApiBaseModel):
    connection_id: str
    namespace_definition: Optional[str]
    namespace_format: Optional[str]
    name: Optional[str]
    prefix: Optional[str]
    operation_ids: Optional[List[str]]
    sync_catalog: ConnectionSyncCatalog
    schedule: Optional[ConnectionSchedule]
    schedule_type: Optional[str]
    schedule_data: Optional[ConnectionScheduleData]
    status: str
    resource_requirements: Optional[ResourceRequirements]
    source_catalog_id: Optional[str]


class SlackConfiguration(ApiBaseModel):
    webhook: str


class Notification(ApiBaseModel):
    notificationType: Optional[str]
    send_on_success: Optional[bool]
    send_on_failure: Optional[bool]
    slack_configuration: Optional[SlackConfiguration]
    customerio_configuration: Optional[Dict[str, Any]]


class Workspace(ApiBaseModel):
    workspace_id: Optional[str]
    customer_id: Optional[str]
    email: Optional[str]
    name: Optional[str]
    slug: Optional[str]
    initial_setup_complete: Optional[bool]
    display_setup_wizard: Optional[bool]
    anonimous_data_collection: Optional[bool]
    news: Optional[bool]
    security_updates: Optional[bool]
    notifications: List[Notification]
    first_completed_sync: Optional[bool]
    feedback_done: Optional[bool]


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
    name: Optional[str]
    namespace_definition: Optional[str]
    namespace_format: Optional[str]
    prefix: Optional[str]
    source_id: str
    destination_id: str
    operation_ids: List[str]
    sync_catalog: ConnectionSyncCatalog
    schedule: Optional[ConnectionSchedule]
    schedule_type: Optional[str]
    schedule_data: Optional[ConnectionScheduleData]
    status: Optional[str]
    resource_requirements: Optional[ResourceRequirements]
    source_catalog_id: Optional[str]


class SearchConnectionsRequest(ApiBaseModel):
    connection_id: Optional[str]
    name: Optional[str]
    namespace_definition: Optional[str]
    namespace_format: Optional[str]
    prefix: Optional[str]
    source_id: Optional[str]
    destination_id: Optional[str]
    schedule: Optional[ConnectionSchedule]
    schedule_type: Optional[str]
    schedule_data: Optional[ConnectionScheduleData]
    status: Optional[str]
    source: Optional[Source]
    destination: Optional[Destination]


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
    reset_config: Optional[JobDefinitionResetConfig]


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
    created_at: str
    updated_at: str
    ended_at: str
    bytes_synced: str
    records_synced: str
    total_stats: StreamStat
    stream_stats: List[StreamStatsDefinition]
    failure_summary: JobFailureSummary


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

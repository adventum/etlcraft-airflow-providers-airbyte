from enum import Enum
from re import L
from typing import Any, Dict, Optional

from airbyte_cdk.models import (AirbyteCatalog, AirbyteGlobalState,
                                AirbyteStream as _AirbyteStream, AirbyteStreamState,
                                DestinationSyncMode, StreamDescriptor,
                                SyncMode, AuthSpecification, AdvancedAuth,
                                ConfiguredAirbyteCatalog)
from pydantic import BaseModel, Extra


class JobStatus(Enum):
    RUNNING = 'running'
    SUCCEEDED = "succeeded"
    CANCELLED = "cancelled"
    PENDING = "pending"
    FAILED = "failed"
    ERROR = "error"
    INCOMPLETE = "incomplete"


def to_camel(string: str) -> str:
    return ''.join(
        word.capitalize() if word_n > 0 else word
        for word_n, word in enumerate(string.split('_')))


class ApiBaseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        extra = Extra.allow


class AirbyteStream(ApiBaseModel):

    name: str
    json_schema: Dict[str, Any]
    supported_sync_modes: Optional[list[SyncMode]]
    source_defined_cursor: Optional[bool]
    default_cursor_field: Optional[list[str]]
    source_defined_primary_key: Optional[list[list[str]]]
    namespace: Optional[str]


class GetJobRequest(ApiBaseModel):
    id: int


class Pagination(ApiBaseModel):
    page_size: int
    row_offset: int


class ListJobsRequest(ApiBaseModel):
    config_types: list[str]
    config_id: str
    including_job_id: int
    pagination: Pagination


class ResourceRequirements(ApiBaseModel):
    cpu_request: str
    cpu_limit: str
    memory_request: str
    memory_limit: str

    class Config:
        def alias_generator(field_name): return field_name


class JobSpecificResourceRequirements(ApiBaseModel):
    job_type: str
    resource_requirements: ResourceRequirements


class DefinitionResourceRequirements(ApiBaseModel):
    default: ResourceRequirements
    job_specific: Optional[list[JobSpecificResourceRequirements]]


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
    log_lines: list[str]


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
    operations_ids: list[str]
    sync_catalog: ConfiguredAirbyteCatalog


class CloneDestinationRequest(ApiBaseModel):
    destination_clone_id: str
    destination_configuration: DestinationConfiguration


class GetDestinationDefinitionSpecificationRequest(ApiBaseModel):
    destination_definition_id: str
    workspace_id: str


class ConnectionSchedule(ApiBaseModel):
    time_unit: str
    units: int


class ConnectionScheduleCron(ApiBaseModel):
    cron_expression: str
    cron_timezone: str


class ConnectionScheduleData(ApiBaseModel):
    basic_schedule: ConnectionSchedule
    cron: ConnectionScheduleCron


class ConnectionSyncCatalogStreamConfig(ApiBaseModel):
    sync_mode: SyncMode
    cursor_field: list[str]
    destination_sync_mode: DestinationSyncMode
    primary_key: list[list[str]]
    alias_name: str
    selected: bool


class ConnectionSyncCatalogStream(ApiBaseModel):
    stream: AirbyteStream
    config: ConnectionSyncCatalogStreamConfig


class ConnectionSyncCatalog(ApiBaseModel):
    streams: list[ConnectionSyncCatalogStream]


class UpdateConnectionRequest(ApiBaseModel):
    connection_id: str
    namespace_definition: Optional[str]
    namespace_format: Optional[str]
    name: Optional[str]
    prefix: Optional[str]
    operation_ids: Optional[list[str]]
    sync_catalog: Optional[ConnectionSyncCatalog]
    schedule: Optional[ConnectionSchedule]
    schedule_type: Optional[str]
    schedule_data: ConnectionScheduleData
    status: Optional[str]
    resource_requirements: Optional[ResourceRequirements]
    source_catalog_id: Optional[str]


class SlackConfiguration(ApiBaseModel):
    webhook: str


class Notification(ApiBaseModel):
    notificationType: str
    send_on_success: bool
    send_on_failure: bool
    slack_configuration: SlackConfiguration
    customerio_configuration: Dict[str, Any]


class Workspace(ApiBaseModel):
    workspace_id: str
    customer_id: str
    email: str
    name: str
    slug: str
    initial_setup_complete: bool
    display_setup_wizard: bool
    anonimous_data_collection: Optional[bool]
    news: bool
    security_updates: bool
    notifications: list[Notification]
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
    """ Describes Airbyte connection between source and destination"""

    connection_id: str
    name: str
    namespace_definition: str
    namespace_format: str
    prefix: str
    source_id: str
    destination_id: str
    operation_ids: list[str]
    sync_catalog: ConnectionSyncCatalog
    schedule: Optional[ConnectionSchedule]
    schedule_type: Optional[str]
    schedule_data: Optional[ConnectionScheduleData]
    status: str
    resource_requirements: Optional[ResourceRequirements]
    source_catalog_id: str


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
    stream_state: list[AirbyteStreamState]
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
    streams_to_reset: list[StreamDescriptor]


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
    failures: list[JobFailure]
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
    stream_stats: list[StreamStatsDefinition]
    failure_summary: JobFailureSummary


class JobAttemptLogs(ApiBaseModel):
    log_lines: list[str]


class JobAttempt(ApiBaseModel):
    attempt: JobAttemptDefinition
    logs: JobAttemptLogs


class DetailedJob(ApiBaseModel):
    job: JobDefinition
    attempts: list[JobAttempt]


class Job(ApiBaseModel):
    job: JobDefinition


class CancelJobRequest(ApiBaseModel):
    id: int

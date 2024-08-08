from datetime import datetime, timedelta

from airflow.models import Variable


def etlcraft_variable(variable_id_without_prefix: str, namespace="etlcraft", default_value=None) -> str:
    variable_id = f"{namespace}_{variable_id_without_prefix}"
    try:
        return Variable.get(variable_id)
    except KeyError:
        return default_value


def today_date(input_date_format: str = "%Y-%m-%d") -> str:
    return datetime.now().strftime(input_date_format)


def n_days_ago_date(last_days_count: int, input_date_format: str = "%Y-%m-%d"):
    return (datetime.now() - timedelta(days=last_days_count - 1)).strftime(
        input_date_format
    )


dates_format_pattern_mapping = {
    "^[0-9]{4}-[0-9]{2}-[0-9]{2}$": "%Y-%m-%d",
    "^[0-9]{4}[0-9]{2}[0-9]{2}$": "%Y%m%d",
    "^$|^[0-9]{2}/[0-9]{2}/[0-9]{4}$": "%d/%m/%Y",
    "^$|^[0-9]{4}-[0-9]{2}-[0-9]{2}$": "%Y-%m-%d",
    "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$": "%Y-%m-%dT%H:%M:%SZ",
    "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}$": "%Y-%m-%dT%H:%M:%S",
    "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z?$": "%Y-%m-%dT%H:%M:%SZ",
    "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z|[0-9]{4}-[0-9]{2}-[0-9]{2}$": "%Y-%m-%dT%H:%M:%SZ",
    "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$": "%Y-%m-%dT%H:%M:%SZ",
    "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2}$": "%Y-%m-%dT%H:%M:%S+00:00",
    "^$|^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$": "%Y-%m-%dT%H:%M:%SZ",
    "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$|^$": "%Y-%m-%dT%H:%M:%SZ",
    "^[0-9]{4}-[0-9]{2}-[0-9]{2} ([0-9]{2}:[0-9]{2}:[0-9]{2})?$": "%Y-%m-%d %H:%M:%S%",
    "$|^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$": "%Y-%m-%d %H:%M:%S",
    "^$|^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}$": "%Y-%m-%dT%H:%M:%S",
    "^$|^[0-9]{4}-[0-9]{2}-[0-9]{2}( [0-9]{2}:[0-9]{2}:[0-9]{2})?$": "%Y-%m-%d %H:%M:%S",
    "^[0-9]{4}-[0-9]{2}-[0-9]{2}(T[0-9]{2}:[0-9]{2}:[0-9]{2}Z)?$": "%Y-%m-%dT%H:%M:%SZ",
    "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}Z$": lambda dt: dt.strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    + ".000Z",
    "^\\d{4}\\-(0[1-9]|1[012])\\-(0[1-9]|[12][0-9]|3[01])$": "%Y-%m-%d",
    "^(?:(\\d{4}\\-(0[1-9]|1[012])\\-(0[1-9]|[12][0-9]|3[01]))|)$": "%Y-%m-%d",
}

first_level_date_from_field_names = [
    "date_from",
    "start_date",
    "start_time",
    "replication_start_date",
    "reports_start_date",
    "since",
    "date_ranges_start_date",
]

first_level_date_to_field_names = [
    "date_to",
    "end_date",
    "replication_end_date",
    "reports_end_date",
    "end_time",
    "date_ranges_end_date",
]

lookup_fields_paths_mapping = {
    "date_from": {},
    "date_to": {},
    "date_type_constant": {
        "$.date_range.oneOf[*].properties.date_range_type.const": "$.date_range.date_range_type"
    },
}

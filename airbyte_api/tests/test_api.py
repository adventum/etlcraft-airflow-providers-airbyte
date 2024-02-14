import pytest

from airbyte_api.api import AirbyteApi
from airbyte_api.models import CreateSourceRequest


def test_create_source():
    api = AirbyteApi(auth=("airbyte", "password"))
    source = api.create_source(
        CreateSourceRequest(
            source_definition_id="778daa7c-feaf-4db6-96f3-70fd645acc77",
            name="test_source",
            workspace_id="c88757c1-f370-4cea-8f40-30b7be0f4b38",
            connection_configuration={
                "host": "localhost",
                "port": 5432,
                "username": "test",
                "password": "test",
                "database": "test",
            },
        )
    )
    assert source.source_id == "123"
    assert source.name == "test"
    assert source.source_type == "test"
    assert source.connection_configuration == {
        "host": "localhost",
        "port": 5432,
        "username": "test",
        "password": "test",
        "database": "test",
    }


if __name__ == "__main__":
    test_create_source()

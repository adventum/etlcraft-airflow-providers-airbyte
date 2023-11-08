# Airbyte Airflow Provider ADVM

Обёртка над официальным модулем Airbyte Airflow Provider, дополняющая его функционал.

## airbyte-api

Модуль `airbyte-api` полностью реализует [API-клиент Airbyte](./airbyte_api/api.py) на основе [схемы Airbyte API](https://airbyte-public-api-docs.s3.us-east-2.amazonaws.com/rapidoc-api-docs.html). Клиент включает в себя CRUD-методы для:

- [Рабочих пространств](https://airbyte-public-api-docs.s3.us-east-2.amazonaws.com/rapidoc-api-docs.html#tag--workspace)
- [Определений источников](https://airbyte-public-api-docs.s3.us-east-2.amazonaws.com/rapidoc-api-docs.html#tag--source_definition)
- [Источников](https://airbyte-public-api-docs.s3.us-east-2.amazonaws.com/rapidoc-api-docs.html#tag--source)
- [Определений назначений](https://airbyte-public-api-docs.s3.us-east-2.amazonaws.com/rapidoc-api-docs.html#tag--destination_definition)
- [Назначений](https://airbyte-public-api-docs.s3.us-east-2.amazonaws.com/rapidoc-api-docs.html#tag--destination)
- [Соединений](https://airbyte-public-api-docs.s3.us-east-2.amazonaws.com/rapidoc-api-docs.html#tag--connection)

[Документация клиента Airbyte API](./docs/airbyte_api.api.md)

## airbyte-airflow-provider-advm

Модуль включает в себя:

- [реализацию Airflow-хука](./airbyte_airflow_provider_advm/hook.py) (на основе [API-клиента модуля `airbyte-api`](./airbyte_api/api.py), что позволяет настраивать очень гибкое поведение DAG'ов и операторов).
  - [пример использования в dag'e](./airbyte_airflow_provider_advm/examples/sync_airbyte_connection_by_prefix_dag.py)
  - [документация хука](./docs/airbyte_airflow_provider_advm.hook.md)
- [Airflow-операторы](./airbyte_airflow_provider_advm/operators.py) для трансформации конфигураций Airbyte-соединений:
  - [документация операторов](./docs/airbyte_airflow_provider_advm.operators.md)

## Ссылки

- [whl-пакеты со всеми версиями модуля](./dist/)
- [Airbyte API reference](https://airbyte-public-api-docs.s3.us-east-2.amazonaws.com/)
- [примеры использования модуля в Airflow DAG'ах](./airbyte_airflow_provider_advm/examples/)

## Build

В setup.py меняем версию и выполняем следующие команды:

```sh
pip3 install wheel
python3 setup.py bdist_wheel
```

В папке /dist появится .whl последней версии.

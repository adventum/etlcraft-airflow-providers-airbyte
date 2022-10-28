# Описание DAG'a множественного патча конфига


У нас есть Python-библиотека `airbyte_airflow_provider_advm` для более эффективной и гибкой работы с Airbyte через Airflow-даги. В данном примере представлен DAG, который:

  1. Фильтрует все имеющиеся в Airbyte-инстансе соединения по префиксу
  2. Для каждого найденного по префиксу соединения меняет конфиг на нужные даты
  3. Делает в этих соединениях сброс данных
  4. Запускает для них синхронизацию
 
Полноценный DAG выглядит так:

```python
from airbyte_airflow_provider_advm.hook import AirbyteHook
from airbyte_airflow_provider_advm.operators import AirbyteResetConnectionOperator, AirbyteSourceConfigTransformOperator
from airflow import DAG
from airflow.utils.dates import datetime
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator

dag = DAG(
    dag_id='sync_airbyte_connections_by_prefix',
    start_date=datetime(2022, 9, 8),
    description='Run Sync Airbyte workspace non-deleted connections by their name prefix',
    schedule_interval = '0 3 * * *',
)
# Создаём Airbyte API Hook. В него передаём ID Airflow-соединения с Airbyte.
# С помощью этого хука мы работаем с API Airbyte-инстанса
airbyte_hook = AirbyteHook(
    airbyte_conn_id='default_airbyte_conn'
)

# Вызываем у созданного хука метод get_airbyte_connections_by_prefix_startswith.
# Этот метод возвращает список коннекшонов, в которых префикс начнается с нужной нам строки.
# В него передаём Airbyte Workspace ID и префикс, с которого должны начинаться префиксы искомых
# соединений. Записываем этот список в переменную connections_filtered.
connections_filtered = airbyte_hook.get_airbyte_connections_by_prefix_startswith(
    workspace_id='12345asdv-fab0-12345-8da0-123456abcde',
    prefix_startswith='my_prefix'
)

# Проходимся по списку connections_filtered в цикле for
for connection in connections_filtered:
    for connection in connections_filtered:
    # Для каждого соединения создаём операции:
    #  1) операция изменения конфига соединения
    #  2) операция сброса данных в соединении
    #  3) операция синхронизации соединения

    # Операция, которая модифицирует поля конфигов сорсов найденных соединений (применяет к ним введённый патч)
    transform_config_op = AirbyteSourceConfigTransformOperator(
        dag=dag,
        airbyte_conn_id='default_airbyte_conn',
        task_id=f'{connection.connection_id}__patch_config',
        source_id=connection.source.source_id,
        config_patch={
            "date_from": "2020-01-01",
            "date_to": "2021-01-31"
        },
        delete_fields=["last_n_days"],
        check_config_connection=True,
    )

    # Операция, которая сбрасывает данные в соединении
    reset_data_op = AirbyteResetConnectionOperator(
        dag=dag,
        task_id=f'{connection.connection_id}__reset',
        airbyte_conn_id='default_airbyte_conn',
        connection_id=connection.connection_id,
        asynchronous=False,
        timeout=3600, # 1 час
    )

    # Операция, которая запускает синхронизацию соединения
    trigger_sync_op = AirbyteTriggerSyncOperator(
        dag=dag,
        task_id=f'{connection.connection_id}__sync',
        airbyte_conn_id='default_airbyte_conn'
        connection_id=connection.connection_id,
        asynchronous=False,
        timeout=3600, # 1 час
    )

    transform_config_op >> reset_data_op >> trigger_sync_op
```

Пройдёмся по каждой его строке.
  
## Импорт и настройки DAG'a

Каждый DAG - это Python-файл, поэтому работает он по питоновским правилам синтаксиса и работы с модулями.
В начале каждого файла DAG'a мы импортируем необходимые модули и классы для работы с DAG'ом. Выглядит это так:

```python
from airbyte_airflow_provider_advm.hook import AirbyteHook
from airbyte_airflow_provider_advm.operators import AirbyteResetConnectionOperator, AirbyteSourceConfigTransformOperator
from airflow import DAG
from airflow.utils.dates import datetime
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
```

После импорта модулей нужно объявить python-объект дага с нужными настройками, такими как:
 - `dag_id` - идентификатор DAG'a в Airflow
 - `start_date` - дата начала отсчёта для интервала выполнения. Может быть как дата в прошлом, так и дата в будущем.
 - `description` - человекочитаемое описание DAG'a
 - `schedule_interval` - [CRON-выражение](https://help.eset.com/protect_admin/80/ru-RU/cron_expression.html) интервала выполнения DAG'a. Например, с выражением `0 0 * * *` DAG будет исполняться каждый час в 0 минут 0 секунд.
 - и другие. Подробнее - https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html

Объект дага объявляется для того, чтобы указать операторам, для какого именно дага мы их создаём, а также для того, чтобы передать в него нужные настройки.

Пример объявления DAG-объекта:

```python
dag = DAG(
    dag_id='sync_airbyte_connections_by_prefix',
    start_date=datetime(2022, 9, 8),
    description='Run Sync Airbyte workspace non-deleted connections by their name prefix',
    schedule_interval = '0 0 * * *',
)
```

После объявления дага подключим инстанс Airbyte к дагу по его ID соединения с помощью хука:

```python
airbyte_hook = AirbyteHook(
    airbyte_conn_id='default_airbyte_conn'
)
```

Этот хук позволяет использовать полную реализацию Airbyte API (например, получить список соединений или сорсов, запустить для них Reset или синхронизацию, удалить сорс или соединение, переименовать их и т.д.) из Python и имеет несколько своих встроенных методов для ускорения написания кода.
В него мы передаём `airbyte_conn_id` - это идентификатор Airbyte-соединения в Airflow (не путать с Source+Destination соединением). В этом Airflow-соединении содержатся доступы для Airbyte-инстанса (хост+порт инстанса и его логин+пароль, если инстанс под авторизацией). Его идентификатор можно взять в Airflow во вкладке Admin->Connections в колонке "Conn Id".

## Фильтруем Airbyte-соединения по префиксу

Чтобы отфильтровать Airbyte-соединения по префиксу, используем метод `get_airbyte_connections_by_prefix_startswith` созданного хука. Этот метод возвращает список коннекшонов, в которых префикс начнается с нужной нам строки. Записываем этот список в переменную `connections_filtered`:

```python
connections_filtered = airbyte_hook.get_airbyte_connections_by_prefix_startswith(
    workspace_id='12345asdv-fab0-12345-8da0-123456abcde',
    prefix_startswith='my_prefix'
)
```

Эта функция будет принимать такие аргументы:

  - `workspace_id` - string-идентификатор рабочей области в Airbyte, в которой находятся нужные соединения. В основном, в Airbyte-инстансе рабочая область всегда одна, хотя можно создать и несколько. ID воркспейса можно выдернуть из адресной строки, либо, как мы дальше увидим, можно просто из всех имеющихся воркспейсов взять самый первый.
  - `prefix_startswith` - string-префикс, с которого должны начинаться префиксы искомых source+destination соединений.

> У хука также есть метод `get_airbyte_connections_by_prefix`, который работает точно так же, только ищет точное совпадение префикса, а не только его начала.

## Операции

Мы отфильтровали соединения, с которыми нужно проводить операции. Они хранятся в списке `connections_filtered`. Теперь нужно пройтись по этому списку в цикле `for` и запустить нужные операции:

```python
for connection in connections_filtered:
    # Для каждого соединения создаём операции:
    #  1) операция изменения конфига соединения
    #  2) операция сброса данных в соединении
    #  3) операция синхронизации соединения

    # Операция, которая модифицирует поля конфигов сорсов найденных соединений (применяет к ним введённый патч)
    transform_config_op = AirbyteSourceConfigTransformOperator(
        dag=dag,
        airbyte_conn_id='default_airbyte_conn',
        task_id=f'{connection.connection_id}__patch_config',
        source_id=connection.source.source_id,
        config_patch={
            "date_from": "2020-01-01",
            "date_to": "2021-01-31"
        },
        delete_fields=["last_n_days"],
        check_config_connection=True,
    )

    # Операция, которая сбрасывает данные в соединении
    reset_data_op = AirbyteResetConnectionOperator(
        dag=dag,
        task_id=f'{connection.connection_id}__reset',
        airbyte_conn_id='default_airbyte_conn',
        connection_id=connection.connection_id,
        asynchronous=False,
        timeout=3600, # 1 час
    )

    # Операция, которая запускает синхронизацию соединения
    trigger_sync_op = AirbyteTriggerSyncOperator(
        dag=dag,
        task_id=f'{connection.connection_id}__sync',
        airbyte_conn_id='default_airbyte_conn'
        connection_id=connection.connection_id,
        asynchronous=False,
        timeout=3600, # 1 час
    )

    transform_config_op >> reset_data_op >> trigger_sync_op
```

### AirbyteSourceConfigTransformOperator


Операция, которая модифицирует поля конфигов сорсов найденных соединений (применяет к ним введённый патч):

```python
    transform_config_op = AirbyteSourceConfigTransformOperator(
        dag=dag,
        airbyte_conn_id='default_airbyte_conn',
        task_id=f'{connection.connection_id}__patch_config,
        source_id=connection.source.source_id,
        config_patch={
            "date_from": "2020-01-01",
            "date_to": "2021-01-31"
        },
        delete_fields=["last_n_days"],
        check_config_connection=True,
    )
```

Оператор `AirbyteSourceConfigTransformOperator` сначала полностью модифицирует локальную копию конфига, а только потом отсылает единственный запрос на изменение конфига на сервере Airbyte. Он принимает такие параметры:
  - `dag` - даг, в котором выполянется оператор. Передаём созданный выше даг.
  - `task_id` - идентификатор таска в Airflow. Тут передаём id соединения + строку `__patch_config`
  - `airbyte_conn_id` - идентификатор Airbyte-соединения в Airflow
  - `source_id` - идентификатор сорса в Airbyte
  - `config_patch` - словарь патча. Введённые в него поля перезапишутся в конфиге, заменяя значения при совпадении ключей.
  - `delete_fields` - список полей, которые нужно будет стереть из конфига перед применением патча. Полезно, если, например, в конфиге уже проставлено поле `last_n_days`, и оно нам не нужно после проставления кастомных дат.
  - `check_config_connection` - True или False. Делать ли check после изменения конфига.

### AirbyteResetConnectionOperator

Операция, которая сбрасывает данные в соединении:

```python
    reset_data_op = AirbyteResetConnectionOperator(
        dag=dag,
        task_id=f'{connection.connection_id}__reset',
        airbyte_conn_id='default_airbyte_conn',
        connection_id=connection.connection_id,
        asynchronous=False,
        timeout=3600, # 1 час
    )
```

Оператор `AirbyteResetConnectionOperator` принимает следующие параметры:
  - `dag` - даг, в котором выполянется оператор. Передаём созданный выше даг.
  - `task_id` - идентификатор таска в Airflow. Тут передаём id соединения + строку `__reset`
  - `airbyte_conn_id` - идентификатор Airbyte-соединения в Airflow.
  - `connection_id` - идентификатор source+destinition соединения.
  - `asynchronous` - `True` или `False`. Если `False`, тогда для завершения работы оператора он дожидается полного завершения сброса данных, периодически проверяя статус, только потом отдаёт выполнение следующим операторам. Если `True`, то просто отдаёт серверу команду на выполнение работы и сразу отдаёт выполнение следующим операторам.
  - `timeout` - таймаут в секундах, после которого оператор перестаёт ждать выполнения работы и выкидывает ошибку таймаута. Используется, только если `asynchronous=True`.

### AirbyteTriggerSyncOperator

Операция, которая запускает синхронизацию (выгрузку данных) в source+destination соединении. Работает точно так же, как и оператор сброса данных:

```python
    trigger_sync_op = AirbyteTriggerSyncOperator(
        dag=dag,
        task_id=f'{connection.connection_id}__sync',
        airbyte_conn_id='default_airbyte_conn'
        connection_id=connection.connection_id,
        asynchronous=False,
        timeout=3600, # 1 час
    )
```

# Поля дат конфига

```json

{
  "date_from": "$.date_from",
  "date_format": "%Y-%m-%d",
  "date_to": "$.date_to",
  "conn_name": "Mytarget Spec"
}

{
  "date_from": "$.start_date",
  "date_format": "%Y-%m-%d",
  "date_to": "$.end_date",
  "conn_name": "TikTok Marketing Source Spec"
}

{
  "date_from": "$.date_from",
  "date_format": "%Y-%m-%dT%H:%M:%S",
  "date_to": "$.date_to",
  "conn_name": "Bitrix24 Crm Spec"
}

{
  "date_from": "$.date_from",
  "date_format": "%Y-%m-%d",
  "date_to": "$.date_to",
  "conn_name": "Twitter Spec"
}

{
  "date_from": "$.start_date",
  "date_format": "%Y-%m-%d",
  "date_to": "$.end_date",
  "conn_name": "Google Analytics V4 Spec"
}

{
  "date_from": "$.start_date",
  "date_format": "%d/%m/%Y",
  "date_to": "$.end_date",
  "conn_name": "Calltouch Spec"
}

{
  "date_from": "$.date_from",
  "date_format": "%Y-%m-%d",
  "date_to": "$.date_to",
  "conn_name": "Alytics Spec"
}

{
  "date_from": "$.start_date",
  "date_format": "%Y-%m-%d",
  "date_to": "$.end_date",
  "conn_name": "Google Ads Spec"
}

{
  "date_from": "$.start_date",
  "date_format": "%Y-%m-%d",
  "date_to": "$.end_date",
  "conn_name": "Google Search Console Spec"
}

{
  "date_from": "$.date_from",
  "date_format": "%Y-%m-%d",
  "date_to": "$.date_to",
  "conn_name": "Yandex Metrica Spec"
}

{
  "date_from": "$.date_range.date_from",
  "date_format": "%Y-%m-%d",
  "date_to": "$.date_range.date_to",
  "date_type_constant": "$.date_range.date_range_type",
  "conn_name": "Yandex Direct Spec"
}


{
  "date_from": "$.date_range.date_from",
  "date_format": "%Y-%m-%d",
  "date_to": "$.date_range.date_to",
  "date_type_constant": "$.date_range.date_range_type",
  "conn_name": "Appmetrica Spec"
}

{
  "date_from": "$.date_from",
  "date_format": "%Y-%m-%d",
  "date_to": "$.date_to",
  "conn_name": "Vk Ads Spec"
}

{
  "date_from": "$.date_range.date_from",
  "date_format": "%Y-%m-%d",
  "date_to": "$.date_range.date_to",
  "date_type_constant": "$.date_range.date_range_type",
  "conn_name": "Jagajam Spec"
}

{
  "date_from": "$.start_date",
  "date_format": "%Y-%m-%d %H:%M:%S",
  "date_to": "$.end_date",
  "conn_name": "Appsflyer Spec"
}

{
  "date_from": "$.start_date",
  "date_format": "%Y-%m-%d",
  "date_to": "$.end_date",
  "conn_name": "Snapchat Marketing Spec"
}

{
  "date_from": "$.start_date",
  "date_format": "%Y-%m-%dT%H:%M:%SZ",
  "date_to": "$.end_date",
  "conn_name": "Source Mixpanel Spec"
}

{
  "date_from": "$.date_from",
  "date_format": "%Y-%m-%d",
  "date_to": "$.date_to",
  "conn_name": "Smartcallback Spec"
}
```
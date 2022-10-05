<!-- markdownlint-disable -->

<a href="../.venv/lib/python3.10/site-packages/airbyte_airflow_provider_advm/hook.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `airbyte_airflow_provider_advm.hook`






---

<a href="../.venv/lib/python3.10/site-packages/airbyte_airflow_provider_advm/hook.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AirbyteHook`
Hook for Airbyte API 

:param airbyte_conn_id: Required. The name of the Airflow connection to get  connection information for Airbyte. :param api_version: Optional. Airbyte API version. 

<a href="../.venv/lib/python3.10/site-packages/airbyte_airflow_provider_advm/hook.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    airbyte_conn_id: str = 'airbyte_default',
    api_version: str = 'v1'
) → None
```






---

#### <kbd>property</kbd> log

Returns a logger. 



---

<a href="../.venv/lib/python3.10/site-packages/airbyte_airflow_provider_advm/hook.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `test_connection`

```python
test_connection()
```

Tests the Airbyte connection by hitting the health API 

---

<a href="../.venv/lib/python3.10/site-packages/airbyte_airflow_provider_advm/hook.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `wait_for_job`

```python
wait_for_job(
    job_id: Union[str, int],
    wait_seconds: float = 3,
    timeout: Optional[float] = 3600
) → None
```

Helper method which polls a job to check if it finishes. 

:param job_id: Required. Id of the Airbyte job :param wait_seconds: Optional. Number of seconds between checks. :param timeout: Optional. How many seconds wait for job to be ready.  Used only if ``asynchronous`` is False. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

<!-- markdownlint-disable -->

<a href="../.venv/lib/python3.10/site-packages/airbyte_airflow_provider_advm/operators.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `airbyte_airflow_provider_advm.operators`




**Global Variables**
---------------
- **TYPE_CHECKING**


---

<a href="../.venv/lib/python3.10/site-packages/airbyte_airflow_provider_advm/operators.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AirbyteSourceConfigTransformOperator`




<a href="../.venv/lib/python3.10/site-packages/airflow/models/baseoperator.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    airbyte_conn_id: str = 'airbyte_default',
    source_id: str,
    config_patch: Dict[str, Any],
    api_version: str = 'v1',
    check_config_connection: bool = True,
    **kwargs
) → None
```






---

#### <kbd>property</kbd> dag

Returns the Operator's DAG if set, otherwise raises an error 

---

#### <kbd>property</kbd> dag_id

Returns dag id if it has one or an adhoc + owner 

---

#### <kbd>property</kbd> downstream_list

List of nodes directly downstream 

---

#### <kbd>property</kbd> inherits_from_empty_operator

Used to determine if an Operator is inherited from EmptyOperator 

---

#### <kbd>property</kbd> label





---

#### <kbd>property</kbd> leaves

Required by DAGNode. 

---

#### <kbd>property</kbd> log

Returns a logger. 

---

#### <kbd>property</kbd> node_id





---

#### <kbd>property</kbd> operator_class





---

#### <kbd>property</kbd> operator_name

@property: use a more friendly display name for the operator, if set 

---

#### <kbd>property</kbd> output

Returns reference to XCom pushed by current operator 

---

#### <kbd>property</kbd> priority_weight_total

Total priority weight for the task. It might include all upstream or downstream tasks. 

Depending on the weight rule: 


- WeightRule.ABSOLUTE - only own weight 
- WeightRule.DOWNSTREAM - adds priority weight of all downstream tasks 
- WeightRule.UPSTREAM - adds priority weight of all upstream tasks 

---

#### <kbd>property</kbd> roots

Required by DAGNode. 

---

#### <kbd>property</kbd> task_type

@property: type of the task 

---

#### <kbd>property</kbd> upstream_list

List of nodes directly upstream 



---

<a href="../.venv/lib/python3.10/site-packages/airbyte_airflow_provider_advm/operators.py#L37"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `execute`

```python
execute(context: 'Context') → None
```






---

<a href="../.venv/lib/python3.10/site-packages/airbyte_airflow_provider_advm/operators.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `LookupSourceDatesFieldsOperator`




<a href="../.venv/lib/python3.10/site-packages/airflow/models/baseoperator.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    airbyte_conn_id: str = 'airbyte_default',
    source_id: str,
    date_from_jsonpath: str | None = None,
    date_to_jsonpath: str | None = None,
    date_type_constant_jsonpath: str | None = None,
    api_version: str = 'v1',
    **kwargs
) → None
```






---

#### <kbd>property</kbd> dag

Returns the Operator's DAG if set, otherwise raises an error 

---

#### <kbd>property</kbd> dag_id

Returns dag id if it has one or an adhoc + owner 

---

#### <kbd>property</kbd> downstream_list

List of nodes directly downstream 

---

#### <kbd>property</kbd> inherits_from_empty_operator

Used to determine if an Operator is inherited from EmptyOperator 

---

#### <kbd>property</kbd> label





---

#### <kbd>property</kbd> leaves

Required by DAGNode. 

---

#### <kbd>property</kbd> log

Returns a logger. 

---

#### <kbd>property</kbd> node_id





---

#### <kbd>property</kbd> operator_class





---

#### <kbd>property</kbd> operator_name

@property: use a more friendly display name for the operator, if set 

---

#### <kbd>property</kbd> output

Returns reference to XCom pushed by current operator 

---

#### <kbd>property</kbd> priority_weight_total

Total priority weight for the task. It might include all upstream or downstream tasks. 

Depending on the weight rule: 


- WeightRule.ABSOLUTE - only own weight 
- WeightRule.DOWNSTREAM - adds priority weight of all downstream tasks 
- WeightRule.UPSTREAM - adds priority weight of all upstream tasks 

---

#### <kbd>property</kbd> roots

Required by DAGNode. 

---

#### <kbd>property</kbd> task_type

@property: type of the task 

---

#### <kbd>property</kbd> upstream_list

List of nodes directly upstream 



---

<a href="../.venv/lib/python3.10/site-packages/airbyte_airflow_provider_advm/operators.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `lookup_dates_fields`

```python
lookup_dates_fields(
    source_definition_spec: dict[str, Any]
) → Dict[str, Union[str, NoneType, Dict[str, str]]]
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

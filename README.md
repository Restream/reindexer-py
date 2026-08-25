# The PyReindexer module provides a connector and its auxiliary tools for interaction with Reindexer. Reindexer static library or reindexer-dev package must be installed

* [pyreindexer.rx\_connector](#pyreindexer.rx_connector)
  * [RxConnector](#pyreindexer.rx_connector.RxConnector)
    * [close](#pyreindexer.rx_connector.RxConnector.close)
    * [namespace\_open](#pyreindexer.rx_connector.RxConnector.namespace_open)
    * [namespace\_close](#pyreindexer.rx_connector.RxConnector.namespace_close)
    * [namespace\_drop](#pyreindexer.rx_connector.RxConnector.namespace_drop)
    * [namespace\_truncate](#pyreindexer.rx_connector.RxConnector.namespace_truncate)
    * [namespace\_rename](#pyreindexer.rx_connector.RxConnector.namespace_rename)
    * [namespaces\_enum](#pyreindexer.rx_connector.RxConnector.namespaces_enum)
    * [schema\_set](#pyreindexer.rx_connector.RxConnector.schema_set)
    * [index\_add](#pyreindexer.rx_connector.RxConnector.index_add)
    * [index\_update](#pyreindexer.rx_connector.RxConnector.index_update)
    * [index\_drop](#pyreindexer.rx_connector.RxConnector.index_drop)
    * [item\_insert](#pyreindexer.rx_connector.RxConnector.item_insert)
    * [item\_update](#pyreindexer.rx_connector.RxConnector.item_update)
    * [item\_upsert](#pyreindexer.rx_connector.RxConnector.item_upsert)
    * [item\_delete](#pyreindexer.rx_connector.RxConnector.item_delete)
    * [meta\_put](#pyreindexer.rx_connector.RxConnector.meta_put)
    * [meta\_get](#pyreindexer.rx_connector.RxConnector.meta_get)
    * [meta\_delete](#pyreindexer.rx_connector.RxConnector.meta_delete)
    * [meta\_enum](#pyreindexer.rx_connector.RxConnector.meta_enum)
    * [exec\_sql](#pyreindexer.rx_connector.RxConnector.exec_sql)
    * [new\_transaction](#pyreindexer.rx_connector.RxConnector.new_transaction)
    * [new\_query](#pyreindexer.rx_connector.RxConnector.new_query)
* [pyreindexer.query\_results](#pyreindexer.query_results)
  * [QueryResults](#pyreindexer.query_results.QueryResults)
    * [status](#pyreindexer.query_results.QueryResults.status)
    * [count](#pyreindexer.query_results.QueryResults.count)
    * [total\_count](#pyreindexer.query_results.QueryResults.total_count)
    * [get\_agg\_results](#pyreindexer.query_results.QueryResults.get_agg_results)
    * [get\_explain\_results](#pyreindexer.query_results.QueryResults.get_explain_results)
* [pyreindexer.expressions](#pyreindexer.expressions)
* [pyreindexer.transaction](#pyreindexer.transaction)
  * [Transaction](#pyreindexer.transaction.Transaction)
    * [insert](#pyreindexer.transaction.Transaction.insert)
    * [update](#pyreindexer.transaction.Transaction.update)
    * [update\_query](#pyreindexer.transaction.Transaction.update_query)
    * [upsert](#pyreindexer.transaction.Transaction.upsert)
    * [delete](#pyreindexer.transaction.Transaction.delete)
    * [delete\_query](#pyreindexer.transaction.Transaction.delete_query)
    * [commit](#pyreindexer.transaction.Transaction.commit)
    * [commit\_with\_count](#pyreindexer.transaction.Transaction.commit_with_count)
    * [rollback](#pyreindexer.transaction.Transaction.rollback)
* [pyreindexer.point](#pyreindexer.point)
  * [Point](#pyreindexer.point.Point)
* [pyreindexer.query](#pyreindexer.query)
  * [Query](#pyreindexer.query.Query)
    * [where](#pyreindexer.query.Query.where)
    * [where\_query](#pyreindexer.query.Query.where_query)
    * [where\_subquery](#pyreindexer.query.Query.where_subquery)
    * [where\_composite](#pyreindexer.query.Query.where_composite)
    * [where\_uuid](#pyreindexer.query.Query.where_uuid)
    * [where\_between\_fields](#pyreindexer.query.Query.where_between_fields)
    * [where\_expressions](#pyreindexer.query.Query.where_expressions)
    * [where\_knn](#pyreindexer.query.Query.where_knn)
    * [where\_knn\_string](#pyreindexer.query.Query.where_knn_string)
    * [open\_bracket](#pyreindexer.query.Query.open_bracket)
    * [close\_bracket](#pyreindexer.query.Query.close_bracket)
    * [match](#pyreindexer.query.Query.match)
    * [dwithin](#pyreindexer.query.Query.dwithin)
    * [aggregate\_sum](#pyreindexer.query.Query.aggregate_sum)
    * [aggregate\_avg](#pyreindexer.query.Query.aggregate_avg)
    * [aggregate\_min](#pyreindexer.query.Query.aggregate_min)
    * [aggregate\_max](#pyreindexer.query.Query.aggregate_max)
    * [distinct](#pyreindexer.query.Query.distinct)
    * [aggregate\_facet](#pyreindexer.query.Query.aggregate_facet)
    * [sort](#pyreindexer.query.Query.sort)
    * [sort\_stpoint\_distance](#pyreindexer.query.Query.sort_stpoint_distance)
    * [sort\_stfield\_distance](#pyreindexer.query.Query.sort_stfield_distance)
    * [op\_and](#pyreindexer.query.Query.op_and)
    * [op\_or](#pyreindexer.query.Query.op_or)
    * [op\_not](#pyreindexer.query.Query.op_not)
    * [request\_total](#pyreindexer.query.Query.request_total)
    * [cached\_total](#pyreindexer.query.Query.cached_total)
    * [limit](#pyreindexer.query.Query.limit)
    * [offset](#pyreindexer.query.Query.offset)
    * [debug](#pyreindexer.query.Query.debug)
    * [strict](#pyreindexer.query.Query.strict)
    * [explain](#pyreindexer.query.Query.explain)
    * [with\_rank](#pyreindexer.query.Query.with_rank)
    * [execute](#pyreindexer.query.Query.execute)
    * [delete](#pyreindexer.query.Query.delete)
    * [set\_object](#pyreindexer.query.Query.set_object)
    * [set](#pyreindexer.query.Query.set)
    * [drop](#pyreindexer.query.Query.drop)
    * [expression](#pyreindexer.query.Query.expression)
    * [update](#pyreindexer.query.Query.update)
    * [must\_execute](#pyreindexer.query.Query.must_execute)
    * [get](#pyreindexer.query.Query.get)
    * [inner\_join](#pyreindexer.query.Query.inner_join)
    * [join](#pyreindexer.query.Query.join)
    * [left\_join](#pyreindexer.query.Query.left_join)
    * [merge](#pyreindexer.query.Query.merge)
    * [on](#pyreindexer.query.Query.on)
    * [select\_fields](#pyreindexer.query.Query.select_fields)
    * [functions](#pyreindexer.query.Query.functions)
    * [equal\_position](#pyreindexer.query.Query.equal_position)
* [pyreindexer.index\_search\_params](#pyreindexer.index_search_params)
  * [IndexSearchParamBruteForce](#pyreindexer.index_search_params.IndexSearchParamBruteForce)
  * [IndexSearchParamHnsw](#pyreindexer.index_search_params.IndexSearchParamHnsw)
  * [IndexSearchParamIvf](#pyreindexer.index_search_params.IndexSearchParamIvf)
* [pyreindexer.index\_definition](#pyreindexer.index_definition)
  * [IndexDefinition](#pyreindexer.index_definition.IndexDefinition)

<a id="pyreindexer.rx_connector"></a>

# pyreindexer.rx\_connector

<a id="pyreindexer.rx_connector.RxConnector"></a>

## RxConnector Objects

```python
class RxConnector(RaiserRx)
```

RxConnector provides a binding to Reindexer upon two shared libraries (hereinafter - APIs): 'rawpyreindexerb.so'
    and 'rawpyreindexerc.so'. The first one is aimed at builtin usage. That API embeds Reindexer, so it could
    be used right in-place as is. The second one acts as a lightweight client which establishes a connection to
    Reindexer server via RPC. The APIs interfaces are completely the same.

#### Arguments:
        dsn (string): The connection string which contains a protocol
            Examples: 'builtin:///tmp/pyrx', 'cproto://127.0.0.1:6534/pyrx'

        cproto options:
             fetch_amount (int): The number of items that will be fetched by one operation
             reconnect_attempts (int): Number of reconnection attempts when connection is lost
             net_timeout (`datetime.timedelta`): Connection and database login timeout value [milliseconds]
             enable_compression (bool): Flag enable/disable traffic compression
             start_special_thread (bool): Determines whether to request a special thread of execution
                on the server for this connection
             client_name (string): Proper name of the application (as a client for Reindexer-server)
             sync_rxcoro_count (int): Client concurrency per connection [1..10'000], default 10

        built-in options:
            max_replication_updates_size (int): Max pended replication updates size in bytes
            allocator_cache_limit (int): Recommended maximum free cache size of tcmalloc memory allocator in bytes
            allocator_cache_part (float): Recommended maximum free cache size of tcmalloc memory allocator in
                relation to total Reindexer allocated memory size, in units

#### Attributes:
    api (module): An API module loaded dynamically for Reindexer calls
    rx (int): A memory pointer to the Reindexer instance
    err_code (int): The API error code
    err_msg (string): The API error message

<a id="pyreindexer.rx_connector.RxConnector.close"></a>

### RxConnector.close

```python
def close() -> None
```

Closes the API instance and frees Reindexer resources.
    Also rolls back leftover transactions and destroys leftover queries
    that were not finished yet.
    Do not call `close()` while other threads still use this connector
    (`execute`, item operations, transactions, `new_query`, and so on).

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet

<a id="pyreindexer.rx_connector.RxConnector.namespace_open"></a>

### RxConnector.namespace\_open

```python
def namespace_open(
    namespace: str, timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Opens the specified namespace or creates it if it does not exist

#### Arguments:
    namespace (string): The name of the namespace
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.namespace_close"></a>

### RxConnector.namespace\_close

```python
def namespace_close(
    namespace: str, timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Closes the specified namespace

#### Arguments:
    namespace (string): The name of the namespace
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.namespace_drop"></a>

### RxConnector.namespace\_drop

```python
def namespace_drop(
    namespace: str, timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Drops the specified namespace

#### Arguments:
    namespace (string): The name of the namespace
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.namespace_truncate"></a>

### RxConnector.namespace\_truncate

```python
def namespace_truncate(
    namespace: str, timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Truncates the specified namespace

#### Arguments:
    namespace (string): The name of the namespace
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.namespace_rename"></a>

### RxConnector.namespace\_rename

```python
def namespace_rename(
    old_ns_name: str,
    new_ns_name: str,
    timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Renames the specified namespace

#### Arguments:
    old_ns_name (string): Old name of the namespace
    new_ns_name (string): New name of the namespace
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.namespaces_enum"></a>

### RxConnector.namespaces\_enum

```python
def namespaces_enum(
    enum_not_opened: bool = False,
    timeout: timedelta = timedelta(milliseconds=0)
) -> List[Dict[str, str]]
```

Gets a list of available namespaces

#### Arguments:
    enum_not_opened (bool, optional): An enumeration mode flag. If it is
        set then closed namespaces are in result list too. Defaults to False
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Returns:
    (:obj:`list` of :obj:`dict`): A list of dictionaries which describe each namespace

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.schema_set"></a>

### RxConnector.schema\_set

```python
def schema_set(
    namespace: str,
    schema: Dict,
    timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Sets the schema for the specified namespace

#### Arguments:
    namespace (string): The name of the namespace
    schema (dict): Schema definition
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.index_add"></a>

### RxConnector.index\_add

```python
def index_add(
    namespace: str,
    index_def: Union[IndexDefinition, Dict],
    timeout: timedelta = timedelta(milliseconds=0)
) -> None
```

Adds an index to the specified namespace

#### Arguments:
    namespace (string): The name of the namespace
    index_def (Union[IndexDefinition, dict]): IndexDefinition object | dict with index definition
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.index_update"></a>

### RxConnector.index\_update

```python
def index_update(
    namespace: str,
    index_def: Union[IndexDefinition, Dict],
    timeout: timedelta = timedelta(milliseconds=0)
) -> None
```

Updates an index in the specified namespace

#### Arguments:
    namespace (string): The name of the namespace
    index_def (Union[IndexDefinition, dict]): IndexDefinition object | dict with index definition
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.index_drop"></a>

### RxConnector.index\_drop

```python
def index_drop(
    namespace: str,
    index_name: str,
    timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Drops an index from the specified namespace

#### Arguments:
    namespace (string): The name of the namespace
    index_name (string): A name of an index
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.item_insert"></a>

### RxConnector.item\_insert

```python
def item_insert(
    namespace: str,
    item_def: Dict,
    precepts: List[str] = None,
    timeout: timedelta = timedelta(milliseconds=0)
) -> None
```

Inserts an item with its precepts into the specified namespace

#### Arguments:
    namespace (string): The name of the namespace
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A list of strings representing precepts
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.item_update"></a>

### RxConnector.item\_update

```python
def item_update(
    namespace: str,
    item_def: Dict,
    precepts: List[str] = None,
    timeout: timedelta = timedelta(milliseconds=0)
) -> None
```

Updates an item with its precepts in the specified namespace

#### Arguments:
    namespace (string): The name of the namespace
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A list of strings representing precepts
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.item_upsert"></a>

### RxConnector.item\_upsert

```python
def item_upsert(
    namespace: str,
    item_def: Dict,
    precepts: List[str] = None,
    timeout: timedelta = timedelta(milliseconds=0)
) -> None
```

Updates an item with its precepts in the specified namespace. Creates the item if it does not exist

#### Arguments:
    namespace (string): The name of the namespace
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A list of strings representing precepts
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.item_delete"></a>

### RxConnector.item\_delete

```python
def item_delete(
    namespace: str,
    item_def: Dict,
    timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Deletes an item from the namespace specified

#### Arguments:
    namespace (string): The name of the namespace
    item_def (dict): A dictionary of item definition
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.meta_put"></a>

### RxConnector.meta\_put

```python
def meta_put(
    namespace: str,
    key: str,
    value: str,
    timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Puts metadata into the Reindexer storage for the specified key

#### Arguments:
    namespace (string): The name of the namespace
    key (string): A key in a storage of Reindexer for metadata keeping
    value (string): A metadata for storage
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.meta_get"></a>

### RxConnector.meta\_get

```python
def meta_get(namespace: str,
             key: str,
             timeout: timedelta = timedelta(milliseconds=0)) -> str
```

Gets metadata from the Reindexer storage by the specified key

#### Arguments:
    namespace (string): The name of the namespace
    key (string): A key in a storage of Reindexer where metadata is kept
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Returns:
    string: A metadata value

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.meta_delete"></a>

### RxConnector.meta\_delete

```python
def meta_delete(
    namespace: str, key: str,
    timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Deletes metadata from the Reindexer storage by the specified key

#### Arguments:
    namespace (string): The name of the namespace
    key (string): A key in a storage of Reindexer where metadata is kept
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.meta_enum"></a>

### RxConnector.meta\_enum

```python
def meta_enum(
    namespace: str,
    timeout: timedelta = timedelta(milliseconds=0)) -> List[str]
```

Gets a list of metadata keys from the Reindexer storage

#### Arguments:
    namespace (string): The name of the namespace
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Returns:
    (:obj:`list` of :obj:`str`): A list of all metadata keys

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.exec_sql"></a>

### RxConnector.exec\_sql

```python
def exec_sql(
    query: str,
    timeout: timedelta = timedelta(milliseconds=0)) -> QueryResults
```

Executes an SQL query and returns query results

#### Arguments:
    query (string): An SQL query
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Returns:
    (:obj:`QueryResults`): A QueryResults iterator

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.new_transaction"></a>

### RxConnector.new\_transaction

```python
def new_transaction(
    namespace: str,
    timeout: timedelta = timedelta(milliseconds=0)) -> Transaction
```

Starts a new transaction and returns the transaction object.
    Warning: once a timeout is set, it will apply to all subsequent steps in the transaction.
    Also rolls back transactions that were dropped without `commit()`/`rollback()`
    since the previous `new_transaction()` or `close()`.

#### Arguments:
    namespace (string): The name of the namespace
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Returns:
    (:obj:`Transaction`): A new transaction

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.new_query"></a>

### RxConnector.new\_query

```python
def new_query(namespace: str) -> Query
```

Creates a new query and returns the query object.
    Also frees native resources of Query objects dropped since the previous
    `new_query()` or `close()`.

#### Arguments:
    namespace (string): The name of the namespace

#### Returns:
    (:obj:`Query`): A new query

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet

<a id="pyreindexer.query_results"></a>

# pyreindexer.query\_results

<a id="pyreindexer.query_results.QueryResults"></a>

## QueryResults Objects

```python
class QueryResults()
```

QueryResults is a disposable iterator of Reindexer results for such queries as SELECT etc.
    When the results are fetched the iterator closes and frees a memory of results buffer of Reindexer

#### Attributes:
    api (module): An API module for Reindexer calls
    err_code (int): The API error code
    err_msg (string): The API error message
    qres_wrapper_ptr (int): A memory pointer to Reindexer iterator object
    qres_iter_count (int): A count of results for iterations
    pos (int): The current result position in iterator

<a id="pyreindexer.query_results.QueryResults.status"></a>

### QueryResults.status

```python
def status() -> None
```

Check status

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query_results.QueryResults.count"></a>

### QueryResults.count

```python
def count() -> int
```

Returns a count of results for iterations

#### Returns
    int: A count of results

<a id="pyreindexer.query_results.QueryResults.total_count"></a>

### QueryResults.total\_count

```python
def total_count() -> int
```

Returns a total or cached count of results

#### Returns
    int: A total or cached count of results

<a id="pyreindexer.query_results.QueryResults.get_agg_results"></a>

### QueryResults.get\_agg\_results

```python
def get_agg_results() -> dict
```

Returns aggregation results for the current query

#### Returns
    (:obj:`dict`): Dictionary with all results for the current query

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query_results.QueryResults.get_explain_results"></a>

### QueryResults.get\_explain\_results

```python
def get_explain_results() -> str
```

Returns explain results for the current query

#### Returns
    (string): Formatted string with explain of results for the current query

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.expressions"></a>

# pyreindexer.expressions

<a id="pyreindexer.transaction"></a>

# pyreindexer.transaction

<a id="pyreindexer.transaction.Transaction"></a>

## Transaction Objects

```python
class Transaction(RaiserTx)
```

An object representing the context of a Reindexer transaction

Call `commit()` or `rollback()` explicitly to finish a transaction.
    Dropping the object without that is only a safety net: rollback may be
    deferred until the next `RxConnector.new_transaction()` or `RxConnector.close()`.

#### Attributes:
    api (module): An API module for Reindexer calls
    transaction_wrapper_ptr (int): A memory pointer to Reindexer transaction object
    err_code (int): The API error code
    err_msg (string): The API error message

<a id="pyreindexer.transaction.Transaction.insert"></a>

### Transaction.insert

```python
def insert(item_def: Dict, precepts: List[str] = None) -> None
```

Inserts an item with its precepts to the transaction
    Warning: the timeout set when the transaction was created is used

#### Arguments:
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A list of strings representing precepts

#### Raises:
    TransactionError: Raises with an error message of API return if Transaction is over
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.update"></a>

### Transaction.update

```python
def update(item_def: Dict, precepts: List[str] = None) -> None
```

Updates an item with its precepts to the transaction
    Warning: the timeout set when the transaction was created is used

#### Arguments:
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A list of strings representing precepts

#### Raises:
    TransactionError: Raises with an error message of API return if Transaction is over
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.update_query"></a>

### Transaction.update\_query

```python
def update_query(query: Query) -> None
```

Updates items with the transaction
    Read-committed isolation is available for read operations.
    Changes made in an active transaction are invisible to the other transactions.

#### Arguments:
    query (:obj:`Query`): A query object to modify

#### Raises:
    TransactionError: Raises with an error message of API return if Transaction is over
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.upsert"></a>

### Transaction.upsert

```python
def upsert(item_def: Dict, precepts: List[str] = None) -> None
```

Updates an item with its precepts to the transaction. Creates the item if it does not exist
    Warning: the timeout set when the transaction was created is used

#### Arguments:
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A list of strings representing precepts

#### Raises:
    TransactionError: Raises with an error message of API return if Transaction is over
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.delete"></a>

### Transaction.delete

```python
def delete(item_def: Dict) -> None
```

Deletes an item from the transaction
    Warning: the timeout set when the transaction was created is used

#### Arguments:
    item_def (dict): A dictionary of item definition

#### Raises:
    TransactionError: Raises with an error message of API return if Transaction is over
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.delete_query"></a>

### Transaction.delete\_query

```python
def delete_query(query: Query)
```

Deletes items with the transaction
    Read-committed isolation is available for read operations.
    Changes made in an active transaction are invisible to the other transactions.

#### Arguments:
    query (:obj:`Query`): A query object to modify

#### Raises:
    TransactionError: Raises with an error message of API return if Transaction is over
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.commit"></a>

### Transaction.commit

```python
def commit(timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Applies changes and finishes the transaction

#### Arguments:
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    TransactionError: Raises with an error message of API return if Transaction is over
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.commit_with_count"></a>

### Transaction.commit\_with\_count

```python
def commit_with_count(timeout: timedelta = timedelta(milliseconds=0)) -> int
```

Applies changes, finishes the transaction and returns the number of changed items

#### Arguments:
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    TransactionError: Raises with an error message of API return if Transaction is over
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.rollback"></a>

### Transaction.rollback

```python
def rollback(timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Rolls back changes and finishes the transaction

#### Arguments:
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    TransactionError: Raises with an error message of API return if Transaction is over
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.point"></a>

# pyreindexer.point

<a id="pyreindexer.point.Point"></a>

## Point Objects

```python
class Point()
```

An object representing the context of a Reindexer 2D point

#### Attributes:
    x (float): x coordinate of the point
    y (float): y coordinate of the point

<a id="pyreindexer.query"></a>

# pyreindexer.query

<a id="pyreindexer.query.Query"></a>

## Query Objects

```python
class Query(RaiserQuery)
```

An object representing the context of a Reindexer query

Native query resources are freed on the next `RxConnector.new_query()` call
    or on `RxConnector.close()`, not necessarily when the Python object is
    garbage-collected.

#### Attributes:
    api (module): An API module for Reindexer calls
    query_wrapper_ptr (int): A memory pointer to Reindexer query object
    err_code (int): The API error code
    err_msg (string): The API error message
    root (:object: Optional[`Query`]): The root query of the Reindexer query
    join_queries (list[:object:`Query`]): The list of join Reindexer query objects
    merged_queries (list[:object:`Query`]): The list of merged Reindexer query objects

<a id="pyreindexer.query.Query.where"></a>

### Query.where

```python
def where(
    index: str,
    condition: CondType,
    keys: Union[ScalarType, list[ScalarType], tuple[list[ScalarType],
                                                    ...]] = None
) -> Query
```

Adds a where condition to the DB query

#### Arguments:
    index (string): Field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    keys (Union[ScalarType, list[ScalarType], tuple[list[ScalarType], ...]]):
        Value of index to be compared with. For composite indexes keys must be list,
        with value of each sub-index

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.where_query"></a>

### Query.where\_query

```python
def where_query(
    sub_query: Query,
    condition: CondType,
    keys: Union[ScalarType, list[ScalarType], tuple[list[ScalarType],
                                                    ...]] = None
) -> Query
```

Adds a sub-query where condition to the DB query

#### Arguments:
    sub_query (:obj:`Query`): Field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    keys (Union[ScalarType, list[ScalarType], tuple[list[ScalarType], ...]]):
        Value of index to be compared with. For composite indexes keys must be list,
        with value of each sub-index

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.where_subquery"></a>

### Query.where\_subquery

```python
def where_subquery(index: str, condition: CondType, sub_query: Query) -> Query
```

Adds a sub-query where condition to the DB query

#### Arguments:
    index (string): Field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    sub_query (:obj:`Query`): Field name used in condition clause

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.where_composite"></a>

### Query.where\_composite

```python
def where_composite(
    index: str, condition: CondType,
    keys: Union[tuple[ScalarType, ...], tuple[list[ScalarType], ...],
                list[list[ScalarType]], list[tuple[ScalarType, ...]]]
) -> Query
```

Adds a where condition to the DB query for composite indexes

#### Arguments:
    index (string): Field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    keys (Union[
            tuple[ScalarType, ...], tuple[list[ScalarType], ...],
             list[list[ScalarType]], list[tuple[ScalarType, ...]]
        ]): Values of composite index to be compared with (value of each sub-index).
        Supported variants:
            (1, "testval1")
            ([1, "test1"], [2, "test2"])
            [[1, "test1"], [2, "test2"]]
            [(1, "test1"), (2, "test2")]

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.where_uuid"></a>

### Query.where\_uuid

```python
def where_uuid(index: str, condition: CondType,
               keys: Union[UUID, list[UUID]]) -> Query
```

Adds a where condition to the DB query with UUID.
    `index` must be declared as uuid-string index in this case

#### Arguments:
    index (string): Field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    keys (Union[UUID, list[UUID]]): Value of index to be compared with

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.where_between_fields"></a>

### Query.where\_between\_fields

```python
def where_between_fields(first_field: str, condition: CondType,
                         second_field: str) -> Query
```

Adds a where condition comparing two fields to the DB query

#### Arguments:
    first_field (string): First field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    second_field (string): Second field name used in condition clause

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.where_expressions"></a>

### Query.where\_expressions

```python
def where_expressions(left: Expression, condition: CondType,
                      right: Expression) -> Query
```

Adds a where condition with expressions to the DB query

#### Arguments:
    left (Expression): Left expression (Field, FlatArrayLen, SubQuery)
    condition (:enum:`CondType`): Type of condition
    right (Expression): Right expression (Field, Values, Now, SubQuery)

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.where_knn"></a>

### Query.where\_knn

```python
def where_knn(
    index: str, vec: List[float],
    param: Union[IndexSearchParamBruteForce | IndexSearchParamHnsw
                 | IndexSearchParamIvf]
) -> Query
```

Adds a where condition to the DB query with a float_vector as args.
    `index` must be declared as float_vector index in this case

#### Arguments:
    index (string): Field name used in condition clause (only float_vector)
    vec (list[float]): KNN value of index to be compared with
    param (:obj:`Union[IndexSearchParamBruteForce|IndexSearchParamHnsw|IndexSearchParamIvf]`):
        KNN search parameters

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    QueryError: Raises with an error message if no vec are specified
    QueryError: Raises with an error message if no param are specified or have an invalid value
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.where_knn_string"></a>

### Query.where\_knn\_string

```python
def where_knn_string(
    index: str, value: str,
    param: Union[IndexSearchParamBruteForce | IndexSearchParamHnsw
                 | IndexSearchParamIvf]
) -> Query
```

Adds a where condition to the DB query with a string as args.
    `index` must be declared as float_vector index in this case.
    WARNING: Only relevant if automatic embedding is configured for this float_vector index

#### Arguments:
    index (string): Field name used in condition clause (only float_vector)
    value (string): value to be generated using automatic embedding of KNN index value to be compared to
    param (:obj:`Union[IndexSearchParamBruteForce|IndexSearchParamHnsw|IndexSearchParamIvf]`):
        KNN search parameters

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    QueryError: Raises with an error message if no value are specified
    QueryError: Raises with an error message if no param are specified or have an invalid value
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.open_bracket"></a>

### Query.open\_bracket

```python
def open_bracket() -> Query
```

Opens a bracket for the where condition in the DB query

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.close_bracket"></a>

### Query.close\_bracket

```python
def close_bracket() -> Query
```

Closes a bracket for the where condition in the DB query

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.match"></a>

### Query.match

```python
def match(index: str, *keys: str) -> Query
```

Adds a string EQ-condition to the DB query

#### Arguments:
    index (string): Field name used in condition clause
    keys (*string): Value of index to be compared with. For composite indexes keys must be list,
        with value of each sub-index

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.dwithin"></a>

### Query.dwithin

```python
def dwithin(index: str, point: Point, distance: float) -> Query
```

Adds a DWithin condition to the DB query

#### Arguments:
    index (string): Field name used in condition clause
    point (:obj:`Point`): Point object used in condition clause
    distance (float): Distance in meters between point

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.aggregate_sum"></a>

### Query.aggregate\_sum

```python
def aggregate_sum(index: str) -> Query
```

Performs a summation of values for a specified index

#### Arguments:
    index (string): Field name for sum operation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.aggregate_avg"></a>

### Query.aggregate\_avg

```python
def aggregate_avg(index: str) -> Query
```

Finds the average at the specified index

#### Arguments:
    index (string): Field name for sum operation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.aggregate_min"></a>

### Query.aggregate\_min

```python
def aggregate_min(index: str) -> Query
```

Finds the minimum at the specified index

#### Arguments:
    index (string): Field name for sum operation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.aggregate_max"></a>

### Query.aggregate\_max

```python
def aggregate_max(index: str) -> Query
```

Finds the maximum at the specified index

#### Arguments:
    index (string): Field name for sum operation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.distinct"></a>

### Query.distinct

```python
def distinct(*fields: str) -> Query
```

Gets distinct values for the specified fields. Applicable to multiple data fields

#### Arguments:
    fields (*string): Field names for distinct, fields should not be empty

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.aggregate_facet"></a>

### Query.aggregate\_facet

```python
def aggregate_facet(*fields: str) -> Query._AggregateFacet
```

Gets facet values for the specified fields. Applicable to multiple data fields and the result of that could be sorted
    by any data column or `count` and cut off by offset and limit. In order to support this functionality,
    this method returns _AggregateFacet which has methods sort, limit and offset

#### Arguments:
    fields (*string): Field names for facet, fields should not be empty

#### Returns:
    (:obj:`_AggregateFacet`): Request object for further customizations

<a id="pyreindexer.query.Query.sort"></a>

### Query.sort

```python
def sort(
    index: str,
    desc: bool = False,
    forced_sort_values: Union[ScalarType, list[ScalarType],
                              tuple[list[ScalarType], ...]] = None
) -> Query
```

Applies a sort order to the returned items. If forced_sort_values argument specified, then items equal to
    values, if found will be placed in the top positions. Forced sort is support for the first sorting field
    only

#### Arguments:
    index (string): The index name
    desc (bool): Sort in descending order
    forced_sort_values (Union[ScalarType, list[ScalarType], tuple[list[ScalarType], ...]]):
        Value of index to match. For composite indexes keys must be list, with value of each sub-index

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.sort_stpoint_distance"></a>

### Query.sort\_stpoint\_distance

```python
def sort_stpoint_distance(index: str, point: Point, desc: bool) -> Query
```

Applies a geometry sort order to the returned items based on the shortest distance
    between geometry field and point (ST_Distance)

#### Arguments:
    index (string): The index name
    point (:obj:`Point`): Point object used in sorting operation
    desc (bool): Sort in descending order

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.sort_stfield_distance"></a>

### Query.sort\_stfield\_distance

```python
def sort_stfield_distance(first_field: str, second_field: str,
                          desc: bool) -> Query
```

Applies a geometry sort order to the returned items based on the shortest distance
    between 2 geometry fields (ST_Distance)

#### Arguments:
    first_field (string): First field name used in condition
    second_field (string): Second field name used in condition
    desc (bool): Sort in descending order

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.op_and"></a>

### Query.op\_and

```python
def op_and() -> Query
```

The next condition will be added with AND.
    This is the default operation for WHERE statements and does not need to be called explicitly.
    Used in DSL conversion

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.op_or"></a>

### Query.op\_or

```python
def op_or() -> Query
```

The next condition will be added with OR.
    Implements short-circuiting:
    if the previous condition evaluates to true, the next will not be evaluated (except for Join conditions)

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.op_not"></a>

### Query.op\_not

```python
def op_not() -> Query
```

The next condition will be added with NOT AND.
    Implements short-circuiting: if the previous condition evaluates to false, the next will not be evaluated

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.request_total"></a>

### Query.request\_total

```python
def request_total() -> Query
```

Requests the calculation of the total number of items

#### Arguments:
    total_name (string, optional): Name to be requested

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.cached_total"></a>

### Query.cached\_total

```python
def cached_total() -> Query
```

Requests the cached calculation of the total number of items

#### Arguments:
    total_name (string, optional): Name to be requested

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.limit"></a>

### Query.limit

```python
def limit(limit_items: int) -> Query
```

Sets a limit on the number of returned items. Analogous to SQL LIMIT

#### Arguments:
    limit_items (int): Number of rows to get from result set

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.offset"></a>

### Query.offset

```python
def offset(start_offset: int) -> Query
```

Sets the offset for the first selected row in the query result

#### Arguments:
    limit_items (int): Index of the first row to get from result set

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.debug"></a>

### Query.debug

```python
def debug(level: LogLevel) -> Query
```

Changes the debug log level on the server

#### Arguments:
    level (:enum:`LogLevel`): Debug log level on server

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.strict"></a>

### Query.strict

```python
def strict(mode: StrictMode) -> Query
```

Changes the strict mode

#### Arguments:
    mode (:enum:`StrictMode`): Strict mode

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.explain"></a>

### Query.explain

```python
def explain() -> Query
```

Enables query explanation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.with_rank"></a>

### Query.with\_rank

```python
def with_rank() -> Query
```

Outputs the fulltext/float_vector rank. Allowed only with fulltext and KNN queries

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.execute"></a>

### Query.execute

```python
def execute(timeout: timedelta = timedelta(milliseconds=0)) -> QueryResults
```

Executes a select query

#### Arguments:
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Returns:
    (:obj:`QueryResults`): A QueryResults iterator

#### Raises:
    ApiError: Raises with an error message when query is in an invalid state
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.delete"></a>

### Query.delete

```python
def delete(timeout: timedelta = timedelta(milliseconds=0)) -> int
```

Executes the query and deletes the matching items

#### Arguments:
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Returns:
    (int): Number of deleted elements

#### Raises:
    QueryError: Raises with an error message when query is in an invalid state
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.set_object"></a>

### Query.set\_object

```python
def set_object(field: str, values: list[ScalarType]) -> Query
```

Adds an object field update to the query

#### Arguments:
    field (string): Field name
    values (list[ScalarType]): List of values to add

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    QueryError: Raises with an error message if no values are specified
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.set"></a>

### Query.set

```python
def set(field: str, values: list[ScalarType]) -> Query
```

Adds a field update to the query

#### Arguments:
    field (string): Field name
    values (list[ScalarType]): List of values to add

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.drop"></a>

### Query.drop

```python
def drop(index: str) -> Query
```

Drops a field from the items

#### Arguments:
    index (string): Field name for drop operation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.expression"></a>

### Query.expression

```python
def expression(field: str, value: str) -> Query
```

Updates an indexed field using an arithmetical expression

#### Arguments:
    field (string): Field name
    value (string): New value expression for field

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.update"></a>

### Query.update

```python
def update(timeout: timedelta = timedelta(milliseconds=0)) -> QueryResults
```

Executes the update query, modifying the fields in the matching items

#### Arguments:
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Returns:
    (:obj:`QueryResults`): A QueryResults iterator

#### Raises:
    QueryError: Raises with an error message when query is in an invalid state
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.must_execute"></a>

### Query.must\_execute

```python
def must_execute(timeout: timedelta = timedelta(
    milliseconds=0)) -> QueryResults
```

Executes the query with a status check

#### Arguments:
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Returns:
    (:obj:`QueryResults`): A QueryResults iterator

#### Raises:
    ApiError: Raises with an error message when query is in an invalid state
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.get"></a>

### Query.get

```python
def get(timeout: timedelta = timedelta(milliseconds=0)) -> (str, bool)
```

Executes the query and returns a single JSON item

#### Arguments:
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Returns:
    (:tuple:string,bool): 1st string item and found flag

#### Raises:
    ApiError: Raises with an error message when query is in an invalid state
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.inner_join"></a>

### Query.inner\_join

```python
def inner_join(query: Query, field: str) -> Query
```

Joins two queries.
    Items from this query are filtered by and expanded with the data from the given query

#### Arguments:
    query (:obj:`Query`): Query object to left join
    field (string): Joined field name. As unique identifier for the join between this query and `join_query`.
        Parameter in order for InnerJoin to work: namespace of `query` contains `field` as one of its fields
        marked as `joined`

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.join"></a>

### Query.join

```python
def join(query: Query, field: str) -> Query
```

Alias for `left_join`. Joins two queries.
    Items from this query are expanded with the data from the given query

#### Arguments:
    query (:obj:`Query`): Query object to left join
    field (string): Joined field name. As unique identifier for the join between this query and `join_query`

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.left_join"></a>

### Query.left\_join

```python
def left_join(join_query: Query, field: str) -> Query
```

Joins two queries.
    Items from this query are expanded with the data from the join_query.
    One of the conditions below must hold for `field` parameter in order for LeftJoin to work:
        namespace of `join_query` contains `field` as one of its fields marked as `joined`

#### Arguments:
    query (:obj:`Query`): Query object to left join
    field (string): Joined field name. As unique identifier for the join between this query and `join_query`

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.merge"></a>

### Query.merge

```python
def merge(query: Query) -> Query
```

Merges queries of the same type

#### Arguments:
    query (:obj:`Query`): Query object to merge

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.on"></a>

### Query.on

```python
def on(index: str, condition: CondType, join_index: str) -> Query
```

On specifies join condition

#### Arguments:
    index (string): Field name from `Query` namespace should be used during join
    condition (:enum:`CondType`): Type of condition, specifies how `Query` will be joined with the latest join query issued on `Query` (e.g. `EQ`/`GT`/`SET`/...)
    join_index (string): Index-field name from namespace for the latest join query issued on `Query` should be used during join

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    QueryError: Raises with an error message when query is in an invalid state

<a id="pyreindexer.query.Query.select_fields"></a>

### Query.select\_fields

```python
def select_fields(*fields: str) -> Query
```

Sets the list of columns to be selected.
    The columns should be specified in the same case as the jsonpaths corresponding to them.
    Non-existent fields and fields in the wrong case are ignored.
    If there are no fields in this list that meet these conditions, then the filter works as "*"

#### Arguments:
    fields (*string): List of columns to be selected

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.functions"></a>

### Query.functions

```python
def functions(*functions: str) -> Query
```

Adds SQL functions to the query

#### Arguments:
    functions (*string): Functions declaration

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.equal_position"></a>

### Query.equal\_position

```python
def equal_position(*equal_position: str) -> Query
```

Adds equal position fields to array queries

#### Arguments:
    equal_poses (*string): Equal position fields to arrays queries

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.index_search_params"></a>

# pyreindexer.index\_search\_params

<a id="pyreindexer.index_search_params.IndexSearchParamBruteForce"></a>

## IndexSearchParamBruteForce Objects

```python
class IndexSearchParamBruteForce()
```

Index search param for brute force index. Equal to basic parameters

#### Attributes:
    k (int): Expected size of KNN index results. Should not be less than 1
    radius (float): In addition to the parameter `k`, the query results can also be filtered by a `rank` -
        value using the parameter, witch called `radius`. It's named so because, under the `L2`-metric,
        it restricts vectors from query result to a sphere of the specified radius

<a id="pyreindexer.index_search_params.IndexSearchParamHnsw"></a>

## IndexSearchParamHnsw Objects

```python
class IndexSearchParamHnsw()
```

Index search param for HNSW index.

#### Attributes:
    k (int): Expected size of KNN index results. Should not be less than 1
    ef (int): Size of nearest neighbor buffer that will be filled during fetching. Should not be less than 'k',
        good story when `ef` ~= 1.5 * `k`
    radius (float): In addition to the parameter `k`, the query results can also be filtered by a `rank` -
        value using the parameter, witch called `radius`. It's named so because, under the `L2`-metric,
        it restricts vectors from query result to a sphere of the specified radius

    If neither `k` nor `radius` are specified, query is considered as streaming
    and response could be limited via limit/offset

<a id="pyreindexer.index_search_params.IndexSearchParamIvf"></a>

## IndexSearchParamIvf Objects

```python
class IndexSearchParamIvf()
```

Index search param for IVF index.

#### Attributes:
    k (int): Expected size of KNN index results. Should not be less than 1
    nprobe (int): Number of centroids that will be scanned in where. Should not be less than 1
    radius (float): In addition to the parameter `k`, the query results can also be filtered by a `rank` -
        value using the parameter, witch called `radius`. It's named so because, under the `L2`-metric,
        it restricts vectors from query result to a sphere of the specified radius

<a id="pyreindexer.index_definition"></a>

# pyreindexer.index\_definition

<a id="pyreindexer.index_definition.IndexDefinition"></a>

## IndexDefinition Objects

```python
class IndexDefinition()
```

IndexDefinition allows to construct and manage indexes more efficiently using a fluent interface

#### Examples:
    ### Create:
        - idx = IndexDefinition(name='test_index', field_type='string', index_type='hash', is_pk=True)
            OR
        - idx = IndexDefinition().name('test_index').field_type('string').index_type('hash').is_pk()
    ### Update:
        - idx['collate_mode'] = 'utf8'
            OR
        - idx.collate_mode('utf8')
            OR
        - idx.update({'collate_mode': 'utf8'})
    ### Get attribute value (only dict-like syntax):
        - idx_name = idx['name']

#### Arguments:
    name (str): An index name
    json_paths (list[str]): JSON paths for mapping values to fields
    field_type (str): Field type. Possible values: `int`, `int64`, `double`, `string`, `bool`, 
        `uuid`, `point`, `composite`, `float_vector`
    index_type (str): Index type. Possible values: `hash`, `tree`, `text`, `-`, `rtree`, 
        `hnsw`, `vec_bf`, `ivf`
    is_pk (bool): True if field is a primary key
    is_array (bool): True if index is an array
    is_dense (bool): True if index is dense - reduce the index size,
        but for tree and hash indexes with low selectivity can seriously decrease update performance
    is_sparse (bool): True if index value may be absent
    is_no_column (bool): True to disable column subindex - reduces the index size, but may also reduce performance
    collate_mode (str): Collation order. Possible values: `none`, `ascii`, `utf8`, `numeric`, `custom`
    sort_order_letters (str): Custom sort order for `collate_mode='custom'`
    config (dict): Config for fulltext or float_vector engines
        [More about `fulltext`](https://github.com/Restream/reindexer/blob/master/fulltext.md)
        [More about `float_vector`](https://github.com/Restream/reindexer/blob/master/float_vector.md)
    expire_after (int): TTL in seconds
    rtree_type (str): RTree index type. Possible values: `rstar`, `linear`, `quadratic`, `greene`


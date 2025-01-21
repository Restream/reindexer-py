# The PyReindexer module provides a connector and its auxiliary tools for interaction with Reindexer

* [pyreindexer.rx\_connector](#pyreindexer.rx_connector)
  * [RxConnector](#pyreindexer.rx_connector.RxConnector)
    * [close](#pyreindexer.rx_connector.RxConnector.close)
    * [namespace\_open](#pyreindexer.rx_connector.RxConnector.namespace_open)
    * [namespace\_close](#pyreindexer.rx_connector.RxConnector.namespace_close)
    * [namespace\_drop](#pyreindexer.rx_connector.RxConnector.namespace_drop)
    * [namespaces\_enum](#pyreindexer.rx_connector.RxConnector.namespaces_enum)
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
    * [select](#pyreindexer.rx_connector.RxConnector.select)
    * [new\_transaction](#pyreindexer.rx_connector.RxConnector.new_transaction)
    * [new\_query](#pyreindexer.rx_connector.RxConnector.new_query)
* [pyreindexer.query\_results](#pyreindexer.query_results)
  * [QueryResults](#pyreindexer.query_results.QueryResults)
    * [status](#pyreindexer.query_results.QueryResults.status)
    * [count](#pyreindexer.query_results.QueryResults.count)
    * [total\_count](#pyreindexer.query_results.QueryResults.total_count)
    * [get\_agg\_results](#pyreindexer.query_results.QueryResults.get_agg_results)
    * [get\_explain\_results](#pyreindexer.query_results.QueryResults.get_explain_results)
* [pyreindexer.transaction](#pyreindexer.transaction)
  * [Transaction](#pyreindexer.transaction.Transaction)
    * [insert](#pyreindexer.transaction.Transaction.insert)
    * [update](#pyreindexer.transaction.Transaction.update)
    * [upsert](#pyreindexer.transaction.Transaction.upsert)
    * [delete](#pyreindexer.transaction.Transaction.delete)
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
    * [open\_bracket](#pyreindexer.query.Query.open_bracket)
    * [close\_bracket](#pyreindexer.query.Query.close_bracket)
    * [match](#pyreindexer.query.Query.match)
    * [dwithin](#pyreindexer.query.Query.dwithin)
    * [distinct](#pyreindexer.query.Query.distinct)
    * [aggregate\_sum](#pyreindexer.query.Query.aggregate_sum)
    * [aggregate\_avg](#pyreindexer.query.Query.aggregate_avg)
    * [aggregate\_min](#pyreindexer.query.Query.aggregate_min)
    * [aggregate\_max](#pyreindexer.query.Query.aggregate_max)
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
    * [select](#pyreindexer.query.Query.select)
    * [functions](#pyreindexer.query.Query.functions)
    * [equal\_position](#pyreindexer.query.Query.equal_position)
* [pyreindexer.index\_definition](#pyreindexer.index_definition)
  * [IndexDefinition](#pyreindexer.index_definition.IndexDefinition)

<a id="pyreindexer.rx_connector"></a>

# pyreindexer.rx\_connector

<a id="pyreindexer.rx_connector.RxConnector"></a>

## RxConnector Objects

```python
class RxConnector(RaiserMixin)
```

RxConnector provides a binding to Reindexer upon two shared libraries (hereinafter - APIs): 'rawpyreindexerb.so'
    and 'rawpyreindexerc.so'. The first one is aimed to a builtin way usage. That API embeds Reindexer, so it could
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
             sync_rxcoro_count (int): Client concurrency per connection

        built-in options:
            max_replication_updates_size (int): Max pended replication updates size in bytes
            allocator_cache_limit (int): Recommended maximum free cache size of tcmalloc memory allocator in bytes
            allocator_cache_part (float): Recommended maximum free cache size of tcmalloc memory allocator in
                relation to total Reindexer allocated memory size, in units

#### Attributes:
    api (module): An API module loaded dynamically for Reindexer calls
    rx (int): A memory pointer to Reindexer instance
    err_code (int): The API error code
    err_msg (string): The API error message

<a id="pyreindexer.rx_connector.RxConnector.close"></a>

### RxConnector.close

```python
def close() -> None
```

Closes an API instance with Reindexer resources freeing

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet

<a id="pyreindexer.rx_connector.RxConnector.namespace_open"></a>

### RxConnector.namespace\_open

```python
def namespace_open(
    namespace: str, timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Opens a namespace specified or creates a namespace if it does not exist

#### Arguments:
    namespace (string): A name of a namespace
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Closes a namespace specified

#### Arguments:
    namespace (string): A name of a namespace
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Drops a namespace specified

#### Arguments:
    namespace (string): A name of a namespace
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.namespaces_enum"></a>

### RxConnector.namespaces\_enum

```python
def namespaces_enum(
    enum_not_opened: bool = False,
    timeout: timedelta = timedelta(milliseconds=0)
) -> List[Dict[str, str]]
```

Gets a list of namespaces available

#### Arguments:
    enum_not_opened (bool, optional): An enumeration mode flag. If it is
        set then closed namespaces are in result list too. Defaults to False
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Returns:
    (:obj:`list` of :obj:`dict`): A list of dictionaries which describe each namespace

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.index_add"></a>

### RxConnector.index\_add

```python
def index_add(
    namespace: str,
    index_def: Dict,
    timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Adds an index to the namespace specified

#### Arguments:
    namespace (string): A name of a namespace
    index_def (dict): A dictionary of index definition
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.index_update"></a>

### RxConnector.index\_update

```python
def index_update(
    namespace: str,
    index_def: Dict,
    timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Updates an index in the namespace specified

#### Arguments:
    namespace (string): A name of a namespace
    index_def (dict): A dictionary of index definition
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Drops an index from the namespace specified

#### Arguments:
    namespace (string): A name of a namespace
    index_name (string): A name of an index
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Inserts an item with its precepts to the namespace specified

#### Arguments:
    namespace (string): A name of a namespace
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A dictionary of index definition
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Updates an item with its precepts in the namespace specified

#### Arguments:
    namespace (string): A name of a namespace
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A dictionary of index definition
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Updates an item with its precepts in the namespace specified. Creates the item if it not exists

#### Arguments:
    namespace (string): A name of a namespace
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A dictionary of index definition
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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
    namespace (string): A name of a namespace
    item_def (dict): A dictionary of item definition
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Puts metadata to a storage of Reindexer by key

#### Arguments:
    namespace (string): A name of a namespace
    key (string): A key in a storage of Reindexer for metadata keeping
    value (string): A metadata for storage
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Gets metadata from a storage of Reindexer by key specified

#### Arguments:
    namespace (string): A name of a namespace
    key (string): A key in a storage of Reindexer where metadata is kept
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Deletes metadata from a storage of Reindexer by key specified

#### Arguments:
    namespace (string): A name of a namespace
    key (string): A key in a storage of Reindexer where metadata is kept
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Gets a list of metadata keys from a storage of Reindexer

#### Arguments:
    namespace (string): A name of a namespace
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Returns:
    (:obj:`list` of :obj:`str`): A list of all metadata keys

#### Raises:
    ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.select"></a>

### RxConnector.select

```python
def select(
    query: str,
    timeout: timedelta = timedelta(milliseconds=0)) -> QueryResults
```

Executes an SQL query and returns query results

#### Arguments:
    query (string): An SQL query
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Starts a new transaction and return the transaction object to processing.
    Warning: once a timeout is set, it will apply to all subsequent steps in the transaction

#### Arguments:
    namespace (string): A name of a namespace
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Creates a new query and return the query object to processing

#### Arguments:
    namespace (string): A name of a namespace

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

<a id="pyreindexer.transaction"></a>

# pyreindexer.transaction

<a id="pyreindexer.transaction.Transaction"></a>

## Transaction Objects

```python
class Transaction()
```

An object representing the context of a Reindexer transaction

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
    precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

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
    precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

#### Raises:
    TransactionError: Raises with an error message of API return if Transaction is over
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.upsert"></a>

### Transaction.upsert

```python
def upsert(item_def: Dict, precepts: List[str] = None) -> None
```

Updates an item with its precepts to the transaction. Creates the item if it not exists
    Warning: the timeout set when the transaction was created is used

#### Arguments:
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

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

<a id="pyreindexer.transaction.Transaction.commit"></a>

### Transaction.commit

```python
def commit(timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Applies changes

#### Arguments:
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    TransactionError: Raises with an error message of API return if Transaction is over
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.commit_with_count"></a>

### Transaction.commit\_with\_count

```python
def commit_with_count(timeout: timedelta = timedelta(milliseconds=0)) -> int
```

Applies changes and return the number of count of changed items

#### Arguments:
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Raises:
    TransactionError: Raises with an error message of API return if Transaction is over
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.rollback"></a>

### Transaction.rollback

```python
def rollback(timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Rollbacks changes

#### Arguments:
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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
class Query()
```

An object representing the context of a Reindexer query

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
        keys: Union[simple_types, tuple[list[simple_types],
                                        ...]] = None) -> Query
```

Adds where condition to DB query with args

#### Arguments:
    index (string): Field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    keys (union[simple_types, (list[simple_types], ...)]):
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
        keys: Union[simple_types, tuple[list[simple_types],
                                        ...]] = None) -> Query
```

Adds sub-query where condition to DB query with args

#### Arguments:
    sub_query (:obj:`Query`): Field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    keys (union[simple_types, (list[simple_types], ...)]):
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

Adds sub-query where condition to DB query

#### Arguments:
    index (string): Field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    sub_query (:obj:`Query`): Field name used in condition clause

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.where_composite"></a>

### Query.where\_composite

```python
def where_composite(index: str, condition: CondType,
                    keys: tuple[list[simple_types], ...]) -> Query
```

Adds where condition to DB query with interface args for composite indexes

#### Arguments:
    index (string): Field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    keys (list[simple_types], ...): Values of composite index to be compared with (value of each sub-index).
        Supported variants:
            ([1, "test1"], [2, "test2"])
            [[1, "test1"], [2, "test2"]])
            ([1, "testval1"], )
            [[1, "testval1"]]
            (1, "testval1")

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.where_uuid"></a>

### Query.where\_uuid

```python
def where_uuid(index: str, condition: CondType, *uuids: UUID) -> Query
```

Adds where condition to DB query with UUID as string args.
    This function applies binary encoding to the UUID value.
    `index` MUST be declared as uuid index in this case

#### Arguments:
    index (string): Field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    uuids (*:obj:`UUID`): Value of index to be compared with. For composite indexes uuids must be list,
        with value of each sub-index

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

Adds comparing two fields where condition to DB query

#### Arguments:
    first_field (string): First field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    second_field (string): Second field name used in condition clause

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.open_bracket"></a>

### Query.open\_bracket

```python
def open_bracket() -> Query
```

Opens bracket for where condition to DB query

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.close_bracket"></a>

### Query.close\_bracket

```python
def close_bracket() -> Query
```

Closes bracket for where condition to DB query

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.match"></a>

### Query.match

```python
def match(index: str, *keys: str) -> Query
```

Adds string EQ-condition to DB query with string args

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

Adds DWithin condition to DB query

#### Arguments:
    index (string): Field name used in condition clause
    point (:obj:`Point`): Point object used in condition clause
    distance (float): Distance in meters between point

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.distinct"></a>

### Query.distinct

```python
def distinct(index: str) -> Query
```

Performs distinct for a certain index. Return only items with uniq value of field

#### Arguments:
    index (string): Field name for distinct operation

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

Finds for the average at the specified index

#### Arguments:
    index (string): Field name for sum operation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.aggregate_min"></a>

### Query.aggregate\_min

```python
def aggregate_min(index: str) -> Query
```

Finds for the minimum at the specified index

#### Arguments:
    index (string): Field name for sum operation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.aggregate_max"></a>

### Query.aggregate\_max

```python
def aggregate_max(index: str) -> Query
```

Finds for the maximum at the specified index

#### Arguments:
    index (string): Field name for sum operation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.aggregate_facet"></a>

### Query.aggregate\_facet

```python
def aggregate_facet(*fields: str) -> Query._AggregateFacet
```

Gets fields facet value. Applicable to multiple data fields and the result of that could be sorted
    by any data column or `count` and cut off by offset and limit. In order to support this functionality
    this method returns AggregationFacetRequest which has methods sort, limit and offset

#### Arguments:
    fields (*string): Fields any data column name or `count`, fields should not be empty

#### Returns:
    (:obj:`_AggregateFacet`): Request object for further customizations

<a id="pyreindexer.query.Query.sort"></a>

### Query.sort

```python
def sort(
    index: str,
    desc: bool = False,
    forced_sort_values: Union[simple_types, tuple[list[simple_types],
                                                  ...]] = None
) -> Query
```

Applies sort order to return from query items. If forced_sort_values argument specified, then items equal to
    values, if found will be placed in the top positions. Forced sort is support for the first sorting field
    only

#### Arguments:
    index (string): The index name
    desc (bool): Sort in descending order
    forced_sort_values (union[simple_types, (list[simple_types], ...)]):
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

Applies geometry sort order to return from query items. Wrapper for geometry sorting by shortest distance
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

Applies geometry sort order to return from query items. Wrapper for geometry sorting by shortest distance
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

Next condition will be added with AND.
    This is the default operation for WHERE statement. Do not have to be called explicitly in user's code.
    Used in DSL conversion

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.op_or"></a>

### Query.op\_or

```python
def op_or() -> Query
```

Next condition will be added with OR.
    Implements short-circuiting:
    if the previous condition is successful the next will not be evaluated, but except Join conditions

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.op_not"></a>

### Query.op\_not

```python
def op_not() -> Query
```

Next condition will be added with NOT AND.
    Implements short-circuiting: if the previous condition is failed the next will not be evaluated

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.request_total"></a>

### Query.request\_total

```python
def request_total() -> Query
```

Requests total items calculation

#### Arguments:
    total_name (string, optional): Name to be requested

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.cached_total"></a>

### Query.cached\_total

```python
def cached_total() -> Query
```

Requests cached total items calculation

#### Arguments:
    total_name (string, optional): Name to be requested

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.limit"></a>

### Query.limit

```python
def limit(limit_items: int) -> Query
```

Sets a limit (count) of returned items. Analog to sql LIMIT rowsNumber

#### Arguments:
    limit_items (int): Number of rows to get from result set

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.offset"></a>

### Query.offset

```python
def offset(start_offset: int) -> Query
```

Sets the number of the first selected row from result query

#### Arguments:
    limit_items (int): Index of the first row to get from result set

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.debug"></a>

### Query.debug

```python
def debug(level: LogLevel) -> Query
```

Changes debug log level on server

#### Arguments:
    level (:enum:`LogLevel`): Debug log level on server

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.strict"></a>

### Query.strict

```python
def strict(mode: StrictMode) -> Query
```

Changes strict mode

#### Arguments:
    mode (:enum:`StrictMode`): Strict mode

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.explain"></a>

### Query.explain

```python
def explain() -> Query
```

Enables explain query

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.with_rank"></a>

### Query.with\_rank

```python
def with_rank() -> Query
```

Outputs fulltext rank. Allowed only with fulltext query

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
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Executes a query, and delete items, matches query

#### Arguments:
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
        A value of 0 disables the timeout (default value)

#### Returns:
    (int): Number of deleted elements

#### Raises:
    QueryError: Raises with an error message when query is in an invalid state
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.set_object"></a>

### Query.set\_object

```python
def set_object(field: str, values: list[simple_types]) -> Query
```

Adds an update query to an object field for an update query

#### Arguments:
    field (string): Field name
    values (list[simple_types]): List of values to add

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    QueryError: Raises with an error message if no values are specified
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.set"></a>

### Query.set

```python
def set(field: str, values: list[simple_types]) -> Query
```

Adds a field update request to the update request

#### Arguments:
    field (string): Field name
    values (list[simple_types]): List of values to add

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.drop"></a>

### Query.drop

```python
def drop(index: str) -> Query
```

Drops a value for a field

#### Arguments:
    index (string): Field name for drop operation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.expression"></a>

### Query.expression

```python
def expression(field: str, value: str) -> Query
```

Updates indexed field by arithmetical expression

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

Executes update query, and update fields in items, which matches query

#### Arguments:
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Executes a query, and update fields in items, which matches query, with status check

#### Arguments:
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Executes a query, and return 1 JSON item

#### Arguments:
    timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
        Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
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

Joins 2 queries.
    Items from the 1-st query are filtered by and expanded with the data from the 2-nd query

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

Join is an alias for LeftJoin. Joins 2 queries.
    Items from this query are expanded with the data from the `query`

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

Joins 2 queries.
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

<a id="pyreindexer.query.Query.select"></a>

### Query.select

```python
def select(*fields: str) -> Query
```

Sets list of columns in this namespace to be finally selected.
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

Adds sql-functions to query

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

Adds equal position fields to arrays queries

#### Arguments:
    equal_poses (*string): Equal position fields to arrays queries

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    ApiError: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.index_definition"></a>

# pyreindexer.index\_definition

<a id="pyreindexer.index_definition.IndexDefinition"></a>

## IndexDefinition Objects

```python
class IndexDefinition(dict)
```

IndexDefinition is a dictionary subclass which allows to construct and manage indexes more efficiently.
NOT IMPLEMENTED YET. USE FIELDS DESCRIPTION ONLY.

#### Arguments:
    name (str): An index name.
    json_paths (:obj:`list` of :obj:`str`): A name for mapping a value to a json field.
    field_type (str): A type of field. Possible values are: `int`, `int64`, `double`, `string`, `bool`, `composite`.
    index_type (str): An index type. Possible values are: `hash`, `tree`, `text`, `-`.
    is_pk (bool): True if a field is a primary key.
    is_array (bool): True if an index is an array.
    is_dense (bool): True if an index is dense. reduce index size. Saves 8 bytes per unique key value for 'hash'
        and 'tree' index types.
        For '-' index type saves 4-8 bytes per each element. Useful for indexes with high selectivity,
        but for tree and hash indexes with low selectivity could
        significantly decrease update performance.
    is_sparse (bool): True if a value of an index may be not presented.
    collate_mode (str): Sets an order of values by collate mode. Possible values are:
        `none`, `ascii`, `utf8`, `numeric`, `custom`.
    sort_order_letters (str): Order for a sort sequence for a custom collate mode.
    config (dict): A config for a fulltext engine.
    [More](https://github.com/Restream/reindexer/blob/master/fulltext.md).


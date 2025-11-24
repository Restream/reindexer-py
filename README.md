# The PyReindexer module provides a connector and its auxiliary tools for interaction with Reindexer. Reindexer static library or reindexer-dev package must be installed

- [The PyReindexer module provides a connector and its auxiliary tools for interaction with Reindexer. Reindexer static library or reindexer-dev package must be installed](#the-pyreindexer-module-provides-a-connector-and-its-auxiliary-tools-for-interaction-with-reindexer-reindexer-static-library-or-reindexer-dev-package-must-be-installed)
- [pyreindexer.rx\_connector](#pyreindexerrx_connector)
  - [RxConnector Objects](#rxconnector-objects)
      - [Arguments](#arguments)
      - [Attributes](#attributes)
    - [RxConnector.close](#rxconnectorclose)
      - [Raises](#raises)
    - [RxConnector.namespace\_open](#rxconnectornamespace_open)
      - [Arguments](#arguments-1)
      - [Raises](#raises-1)
    - [RxConnector.namespace\_close](#rxconnectornamespace_close)
      - [Arguments](#arguments-2)
      - [Raises](#raises-2)
    - [RxConnector.namespace\_drop](#rxconnectornamespace_drop)
      - [Arguments](#arguments-3)
      - [Raises](#raises-3)
    - [RxConnector.namespaces\_enum](#rxconnectornamespaces_enum)
      - [Arguments](#arguments-4)
      - [Returns](#returns)
      - [Raises](#raises-4)
    - [RxConnector.index\_add](#rxconnectorindex_add)
      - [Arguments](#arguments-5)
      - [Raises](#raises-5)
    - [RxConnector.index\_update](#rxconnectorindex_update)
      - [Arguments](#arguments-6)
      - [Raises](#raises-6)
    - [RxConnector.index\_drop](#rxconnectorindex_drop)
      - [Arguments](#arguments-7)
      - [Raises](#raises-7)
    - [RxConnector.item\_insert](#rxconnectoritem_insert)
      - [Arguments](#arguments-8)
      - [Raises](#raises-8)
    - [RxConnector.item\_update](#rxconnectoritem_update)
      - [Arguments](#arguments-9)
      - [Raises](#raises-9)
    - [RxConnector.item\_upsert](#rxconnectoritem_upsert)
      - [Arguments](#arguments-10)
      - [Raises](#raises-10)
    - [RxConnector.item\_delete](#rxconnectoritem_delete)
      - [Arguments](#arguments-11)
      - [Raises](#raises-11)
    - [RxConnector.meta\_put](#rxconnectormeta_put)
      - [Arguments](#arguments-12)
      - [Raises](#raises-12)
    - [RxConnector.meta\_get](#rxconnectormeta_get)
      - [Arguments](#arguments-13)
      - [Returns](#returns-1)
      - [Raises](#raises-13)
    - [RxConnector.meta\_delete](#rxconnectormeta_delete)
      - [Arguments](#arguments-14)
      - [Raises](#raises-14)
    - [RxConnector.meta\_enum](#rxconnectormeta_enum)
      - [Arguments](#arguments-15)
      - [Returns](#returns-2)
      - [Raises](#raises-15)
    - [RxConnector.exec\_sql](#rxconnectorexec_sql)
      - [Arguments](#arguments-16)
      - [Returns](#returns-3)
      - [Raises](#raises-16)
    - [RxConnector.new\_transaction](#rxconnectornew_transaction)
      - [Arguments](#arguments-17)
      - [Returns](#returns-4)
      - [Raises](#raises-17)
    - [RxConnector.new\_query](#rxconnectornew_query)
      - [Arguments](#arguments-18)
      - [Returns](#returns-5)
      - [Raises](#raises-18)
- [pyreindexer.query\_results](#pyreindexerquery_results)
  - [QueryResults Objects](#queryresults-objects)
      - [Attributes](#attributes-1)
    - [QueryResults.status](#queryresultsstatus)
      - [Raises](#raises-19)
    - [QueryResults.count](#queryresultscount)
      - [Returns](#returns-6)
    - [QueryResults.total\_count](#queryresultstotal_count)
      - [Returns](#returns-7)
    - [QueryResults.get\_agg\_results](#queryresultsget_agg_results)
      - [Returns](#returns-8)
      - [Raises](#raises-20)
    - [QueryResults.get\_explain\_results](#queryresultsget_explain_results)
      - [Returns](#returns-9)
      - [Raises](#raises-21)
- [pyreindexer.transaction](#pyreindexertransaction)
  - [Transaction Objects](#transaction-objects)
      - [Attributes](#attributes-2)
    - [Transaction.insert](#transactioninsert)
      - [Arguments](#arguments-19)
      - [Raises](#raises-22)
    - [Transaction.update](#transactionupdate)
      - [Arguments](#arguments-20)
      - [Raises](#raises-23)
    - [Transaction.update\_query](#transactionupdate_query)
      - [Arguments](#arguments-21)
      - [Raises](#raises-24)
    - [Transaction.upsert](#transactionupsert)
      - [Arguments](#arguments-22)
      - [Raises](#raises-25)
    - [Transaction.delete](#transactiondelete)
      - [Arguments](#arguments-23)
      - [Raises](#raises-26)
    - [Transaction.delete\_query](#transactiondelete_query)
      - [Arguments](#arguments-24)
      - [Raises](#raises-27)
    - [Transaction.commit](#transactioncommit)
      - [Arguments](#arguments-25)
      - [Raises](#raises-28)
    - [Transaction.commit\_with\_count](#transactioncommit_with_count)
      - [Arguments](#arguments-26)
      - [Raises](#raises-29)
    - [Transaction.rollback](#transactionrollback)
      - [Arguments](#arguments-27)
      - [Raises](#raises-30)
- [pyreindexer.point](#pyreindexerpoint)
  - [Point Objects](#point-objects)
      - [Attributes](#attributes-3)
- [pyreindexer.query](#pyreindexerquery)
  - [Query Objects](#query-objects)
      - [Attributes](#attributes-4)
    - [Query.where](#querywhere)
      - [Arguments](#arguments-28)
      - [Returns](#returns-10)
      - [Raises](#raises-31)
    - [Query.where\_query](#querywhere_query)
      - [Arguments](#arguments-29)
      - [Returns](#returns-11)
      - [Raises](#raises-32)
    - [Query.where\_subquery](#querywhere_subquery)
      - [Arguments](#arguments-30)
      - [Returns](#returns-12)
    - [Query.where\_composite](#querywhere_composite)
      - [Arguments](#arguments-31)
      - [Returns](#returns-13)
      - [Raises](#raises-33)
    - [Query.where\_uuid](#querywhere_uuid)
      - [Arguments](#arguments-32)
      - [Returns](#returns-14)
      - [Raises](#raises-34)
    - [Query.where\_between\_fields](#querywhere_between_fields)
      - [Arguments](#arguments-33)
      - [Returns](#returns-15)
    - [Query.where\_knn](#querywhere_knn)
      - [Arguments](#arguments-34)
      - [Returns](#returns-16)
      - [Raises](#raises-35)
    - [Query.where\_knn\_string](#querywhere_knn_string)
      - [Arguments](#arguments-35)
      - [Returns](#returns-17)
      - [Raises](#raises-36)
    - [Query.open\_bracket](#queryopen_bracket)
      - [Returns](#returns-18)
      - [Raises](#raises-37)
    - [Query.close\_bracket](#queryclose_bracket)
      - [Returns](#returns-19)
      - [Raises](#raises-38)
    - [Query.match](#querymatch)
      - [Arguments](#arguments-36)
      - [Returns](#returns-20)
      - [Raises](#raises-39)
    - [Query.dwithin](#querydwithin)
      - [Arguments](#arguments-37)
      - [Returns](#returns-21)
    - [Query.distinct](#querydistinct)
      - [Arguments](#arguments-38)
      - [Returns](#returns-22)
    - [Query.aggregate\_sum](#queryaggregate_sum)
      - [Arguments](#arguments-39)
      - [Returns](#returns-23)
    - [Query.aggregate\_avg](#queryaggregate_avg)
      - [Arguments](#arguments-40)
      - [Returns](#returns-24)
    - [Query.aggregate\_min](#queryaggregate_min)
      - [Arguments](#arguments-41)
      - [Returns](#returns-25)
    - [Query.aggregate\_max](#queryaggregate_max)
      - [Arguments](#arguments-42)
      - [Returns](#returns-26)
    - [Query.aggregate\_facet](#queryaggregate_facet)
      - [Arguments](#arguments-43)
      - [Returns](#returns-27)
    - [Query.sort](#querysort)
      - [Arguments](#arguments-44)
      - [Returns](#returns-28)
      - [Raises](#raises-40)
    - [Query.sort\_stpoint\_distance](#querysort_stpoint_distance)
      - [Arguments](#arguments-45)
      - [Returns](#returns-29)
    - [Query.sort\_stfield\_distance](#querysort_stfield_distance)
      - [Arguments](#arguments-46)
      - [Returns](#returns-30)
      - [Raises](#raises-41)
    - [Query.op\_and](#queryop_and)
      - [Returns](#returns-31)
    - [Query.op\_or](#queryop_or)
      - [Returns](#returns-32)
    - [Query.op\_not](#queryop_not)
      - [Returns](#returns-33)
    - [Query.request\_total](#queryrequest_total)
      - [Arguments](#arguments-47)
      - [Returns](#returns-34)
    - [Query.cached\_total](#querycached_total)
      - [Arguments](#arguments-48)
      - [Returns](#returns-35)
    - [Query.limit](#querylimit)
      - [Arguments](#arguments-49)
      - [Returns](#returns-36)
    - [Query.offset](#queryoffset)
      - [Arguments](#arguments-50)
      - [Returns](#returns-37)
    - [Query.debug](#querydebug)
      - [Arguments](#arguments-51)
      - [Returns](#returns-38)
    - [Query.strict](#querystrict)
      - [Arguments](#arguments-52)
      - [Returns](#returns-39)
    - [Query.explain](#queryexplain)
      - [Returns](#returns-40)
    - [Query.with\_rank](#querywith_rank)
      - [Returns](#returns-41)
    - [Query.execute](#queryexecute)
      - [Arguments](#arguments-53)
      - [Returns](#returns-42)
      - [Raises](#raises-42)
    - [Query.delete](#querydelete)
      - [Arguments](#arguments-54)
      - [Returns](#returns-43)
      - [Raises](#raises-43)
    - [Query.set\_object](#queryset_object)
      - [Arguments](#arguments-55)
      - [Returns](#returns-44)
      - [Raises](#raises-44)
    - [Query.set](#queryset)
      - [Arguments](#arguments-56)
      - [Returns](#returns-45)
      - [Raises](#raises-45)
    - [Query.drop](#querydrop)
      - [Arguments](#arguments-57)
      - [Returns](#returns-46)
    - [Query.expression](#queryexpression)
      - [Arguments](#arguments-58)
      - [Returns](#returns-47)
    - [Query.update](#queryupdate)
      - [Arguments](#arguments-59)
      - [Returns](#returns-48)
      - [Raises](#raises-46)
    - [Query.must\_execute](#querymust_execute)
      - [Arguments](#arguments-60)
      - [Returns](#returns-49)
      - [Raises](#raises-47)
    - [Query.get](#queryget)
      - [Arguments](#arguments-61)
      - [Returns](#returns-50)
      - [Raises](#raises-48)
    - [Query.inner\_join](#queryinner_join)
      - [Arguments](#arguments-62)
      - [Returns](#returns-51)
    - [Query.join](#queryjoin)
      - [Arguments](#arguments-63)
      - [Returns](#returns-52)
    - [Query.left\_join](#queryleft_join)
      - [Arguments](#arguments-64)
      - [Returns](#returns-53)
    - [Query.merge](#querymerge)
      - [Arguments](#arguments-65)
      - [Returns](#returns-54)
    - [Query.on](#queryon)
      - [Arguments](#arguments-66)
      - [Returns](#returns-55)
      - [Raises](#raises-49)
    - [Query.select\_fields](#queryselect_fields)
      - [Arguments](#arguments-67)
      - [Returns](#returns-56)
      - [Raises](#raises-50)
    - [Query.functions](#queryfunctions)
      - [Arguments](#arguments-68)
      - [Returns](#returns-57)
      - [Raises](#raises-51)
    - [Query.equal\_position](#queryequal_position)
      - [Arguments](#arguments-69)
      - [Returns](#returns-58)
      - [Raises](#raises-52)
- [pyreindexer.index\_search\_params](#pyreindexerindex_search_params)
  - [IndexSearchParamBruteForce Objects](#indexsearchparambruteforce-objects)
      - [Attributes](#attributes-5)
  - [IndexSearchParamHnsw Objects](#indexsearchparamhnsw-objects)
      - [Attributes](#attributes-6)
  - [IndexSearchParamIvf Objects](#indexsearchparamivf-objects)
      - [Attributes](#attributes-7)
- [pyreindexer.index\_definition](#pyreindexerindex_definition)
  - [IndexDefinition Objects](#indexdefinition-objects)
      - [Arguments](#arguments-70)

<a id="pyreindexer.rx_connector"></a>

# pyreindexer.rx\_connector

<a id="pyreindexer.rx_connector.RxConnector"></a>

## RxConnector Objects

```python
class RxConnector(RaiserMixin)
```

RxConnector provides a binding to Reindexer upon two shared libraries (hereinafter - APIs): 'rawpyreindexerb.so'
    and 'rawpyreindexerc.so'. The first one is aimed at built-in usage. That API embeds Reindexer, so it could
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

Closes the API instance and frees Reindexer resources

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
        Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
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

Adds an index to the specified namespace

#### Arguments:
    namespace (string): The name of the namespace
    index_def (dict): A dictionary of index definition
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
    index_def: Dict,
    timeout: timedelta = timedelta(milliseconds=0)) -> None
```

Updates an index in the specified namespace

#### Arguments:
    namespace (string): The name of the namespace
    index_def (dict): A dictionary of index definition
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
    precepts (:obj:`list` of :obj:`str`): A dictionary of index definition
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
    precepts (:obj:`list` of :obj:`str`): A dictionary of index definition
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
    precepts (:obj:`list` of :obj:`str`): A dictionary of index definition
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

Puts metadata to a storage of Reindexer by key

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

Gets metadata from a storage of Reindexer by key specified

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

Deletes metadata from a storage of Reindexer by key specified

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

Gets a list of metadata keys from a storage of Reindexer

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

### RxConnector.exec_sql

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

Starts a new transaction and return the transaction object to processing.
    Warning: once a timeout is set, it will apply to all subsequent steps in the transaction

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

Creates a new query and return the query object to processing

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

<a id="pyreindexer.transaction.Transaction.update_query"></a>

### Transaction.update\_query

```python
def update_query(query: Query) -> None
```

Updates items with the transaction
    Read-committed isolation is available for read operations.
    Changes made in active transaction is invisible to current and another transactions.

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

<a id="pyreindexer.transaction.Transaction.delete_query"></a>

### Transaction.delete\_query

```python
def delete_query(query: Query)
```

Deletes items with the transaction
    Read-committed isolation is available for read operations.
    Changes made in active transaction is invisible to current and another transactions.

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

Applies changes

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

Applies changes and return the number of count of changed items

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

Rollbacks changes

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

Adds where condition to DB query with UUID.
    `index` MUST be declared as uuid-string index in this case

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

<a id="pyreindexer.query.Query.where_knn"></a>

### Query.where\_knn

```python
def where_knn(
    index: str, vec: List[float],
    param: Union[IndexSearchParamBruteForce | IndexSearchParamHnsw | IndexSearchParamIvf]
) -> Query
```

Adds where condition to DB query with float_vector as args.
    `index` MUST be declared as float_vector index in this case

#### Arguments:
    index (string): Field name used in condition clause (only float_vector)
    vec (list[float]): KNN value of index to be compared with
    param (:obj:`union[IndexSearchParamBruteForce|IndexSearchParamHnsw|IndexSearchParamIvf]`): KNN search parameters

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
    param: Union[IndexSearchParamBruteForce | IndexSearchParamHnsw | IndexSearchParamIvf]
) -> Query
```

Adds where condition to DB query with string as args.
    `index` MUST be declared as float_vector index in this case.
    WARNING: Only relevant if automatic embedding is configured for this float_vector index

#### Arguments:
    index (string): Field name used in condition clause (only float_vector)
    value (string): value to be generated using automatic embedding of KNN index value to be compared to
    param (:obj:`union[IndexSearchParamBruteForce|IndexSearchParamHnsw|IndexSearchParamIvf]`): KNN search parameters

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

Outputs fulltext/float_vector rank. Allowed only with fulltext and KNN query

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

Executes a query, and delete items, matches query

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

Executes a query, and update fields in items, which matches query, with status check

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

Executes a query, and return 1 JSON item

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

<a id="pyreindexer.query.Query.select_fields"></a>

### Query.select_fields

```python
def select_fields(*fields: str) -> Query
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
      it restricts vectors from query result to a sphere of the specified radius. [More about `radius`]
      (https://github.com/Restream/reindexer/blob/master/float_vector.md)

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
      it restricts vectors from query result to a sphere of the specified radius. [More about `radius`]
      (https://github.com/Restream/reindexer/blob/master/float_vector.md)

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
      it restricts vectors from query result to a sphere of the specified radius. [More about `radius`]
      (https://github.com/Restream/reindexer/blob/master/float_vector.md)

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
    field_type (str): A type of field. Possible values are: `int`, `int64`, `double`, `string`, `bool`,
    `composite`, `float_vector`.
    index_type (str): An index type. Possible values are: `hash`, `tree`, `text`, `-`, `hnsw`, `vec_bf`, `ivf`.
    is_pk (bool): True if a field is a primary key.
    is_array (bool): True if an index is an array.
    is_dense (bool): True if an index is dense. Reduce the index size. Saves 8 bytes per unique key value for 'hash'
        and 'tree' index types. For '-' index type saves 4-8 bytes per each element. Useful for indexes with
        high selectivity, but for tree and hash indexes with low selectivity can seriously decrease update
        performance.
    is_no_column (bool): True if allows to disable column subindex. Reduces the index size.
        Allows to save ~(`stored_type_size` * `namespace_items_count`) bytes, where `stored_type_size` is the size
        of the type stored in the index, and `namespace_items_count` is the number of items in the namespace.
        May reduce performance.
    is_sparse (bool): True if a value of an index may be not presented.
    collate_mode (str): Sets an order of values by collate mode. Possible values are:
        `none`, `ascii`, `utf8`, `numeric`, `custom`.
    sort_order_letters (str): Order for a sort sequence for a custom collate mode.
    config (dict): A config for a fulltext and float_vector engine.
    [More about `fulltext`](https://github.com/Restream/reindexer/blob/master/fulltext.md) or
    [More about `float_vector`](https://github.com/Restream/reindexer/blob/master/float_vector.md).


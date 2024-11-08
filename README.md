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

#### Attributes:
    api (module): An API module loaded dynamically for Reindexer calls
    rx (int): A memory pointer to Reindexer instance
    err_code (int): The API error code
    err_msg (string): The API error message

<a id="pyreindexer.rx_connector.RxConnector.close"></a>

### close

```python
def close() -> None
```

Closes an API instance with Reindexer resources freeing

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet

<a id="pyreindexer.rx_connector.RxConnector.namespace_open"></a>

### namespace\_open

```python
def namespace_open(namespace) -> None
```

Opens a namespace specified or creates a namespace if it does not exist

#### Arguments:
    namespace (string): A name of a namespace

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.namespace_close"></a>

### namespace\_close

```python
def namespace_close(namespace) -> None
```

Closes a namespace specified

#### Arguments:
    namespace (string): A name of a namespace

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.namespace_drop"></a>

### namespace\_drop

```python
def namespace_drop(namespace) -> None
```

Drops a namespace specified

#### Arguments:
    namespace (string): A name of a namespace

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.namespaces_enum"></a>

### namespaces\_enum

```python
def namespaces_enum(enum_not_opened=False) -> List[Dict[str, str]]
```

Gets a list of namespaces available

#### Arguments:
    enum_not_opened (bool, optional): An enumeration mode flag. If it is
        set then closed namespaces are in result list too. Defaults to False

#### Returns:
    (:obj:`list` of :obj:`dict`): A list of dictionaries which describe each namespace

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.index_add"></a>

### index\_add

```python
def index_add(namespace, index_def) -> None
```

Adds an index to the namespace specified

#### Arguments:
    namespace (string): A name of a namespace
    index_def (dict): A dictionary of index definition

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.index_update"></a>

### index\_update

```python
def index_update(namespace, index_def) -> None
```

Updates an index in the namespace specified

#### Arguments:
    namespace (string): A name of a namespace
    index_def (dict): A dictionary of index definition

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.index_drop"></a>

### index\_drop

```python
def index_drop(namespace, index_name) -> None
```

Drops an index from the namespace specified

#### Arguments:
    namespace (string): A name of a namespace
    index_name (string): A name of an index

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.item_insert"></a>

### item\_insert

```python
def item_insert(namespace, item_def, precepts=None) -> None
```

Inserts an item with its precepts to the namespace specified

#### Arguments:
    namespace (string): A name of a namespace
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.item_update"></a>

### item\_update

```python
def item_update(namespace, item_def, precepts=None) -> None
```

Updates an item with its precepts in the namespace specified

#### Arguments:
    namespace (string): A name of a namespace
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.item_upsert"></a>

### item\_upsert

```python
def item_upsert(namespace, item_def, precepts=None) -> None
```

Updates an item with its precepts in the namespace specified. Creates the item if it not exists

#### Arguments:
    namespace (string): A name of a namespace
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.item_delete"></a>

### item\_delete

```python
def item_delete(namespace, item_def) -> None
```

Deletes an item from the namespace specified

#### Arguments:
    namespace (string): A name of a namespace
    item_def (dict): A dictionary of item definition

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.meta_put"></a>

### meta\_put

```python
def meta_put(namespace, key, value) -> None
```

Puts metadata to a storage of Reindexer by key

#### Arguments:
    namespace (string): A name of a namespace
    key (string): A key in a storage of Reindexer for metadata keeping
    value (string): A metadata for storage

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.meta_get"></a>

### meta\_get

```python
def meta_get(namespace, key) -> str
```

Gets metadata from a storage of Reindexer by key specified

#### Arguments:
    namespace (string): A name of a namespace
    key (string): A key in a storage of Reindexer where metadata is kept

#### Returns:
    string: A metadata value

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.meta_delete"></a>

### meta\_delete

```python
def meta_delete(namespace, key) -> None
```

Deletes metadata from a storage of Reindexer by key specified

#### Arguments:
    namespace (string): A name of a namespace
    key (string): A key in a storage of Reindexer where metadata is kept

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.meta_enum"></a>

### meta\_enum

```python
def meta_enum(namespace) -> List[str]
```

Gets a list of metadata keys from a storage of Reindexer

#### Arguments:
    namespace (string): A name of a namespace

#### Returns:
    (:obj:`list` of :obj:`str`): A list of all metadata keys

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.select"></a>

### select

```python
def select(query: str) -> QueryResults
```

Executes an SQL query and returns query results

#### Arguments:
    query (string): An SQL query

#### Returns:
    (:obj:`QueryResults`): A QueryResults iterator

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.new_transaction"></a>

### new\_transaction

```python
def new_transaction(namespace) -> Transaction
```

Starts a new transaction and return the transaction object to processing

#### Arguments:
    namespace (string): A name of a namespace

#### Returns:
    (:obj:`Transaction`): A new transaction

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.rx_connector.RxConnector.new_query"></a>

### new\_query

```python
def new_query(namespace: str) -> Query
```

Creates a new query and return the query object to processing

#### Arguments:
    namespace (string): A name of a namespace

#### Returns:
    (:obj:`Query`): A new query

#### Raises:
    Exception: Raises with an error message when Reindexer instance is not initialized yet

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

### status

```python
def status()
```

Check status

#### Raises:
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query_results.QueryResults.count"></a>

### count

```python
def count()
```

Returns a count of results

# Returns
    int: A count of results

<a id="pyreindexer.query_results.QueryResults.get_agg_results"></a>

### get\_agg\_results

```python
def get_agg_results()
```

Returns aggregation results for the current query

# Returns
    (:obj:`dict`): Dictionary with all results for the current query

#### Raises:
    Exception: Raises with an error message of API return on non-zero error code

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

### insert

```python
def insert(item_def, precepts=None)
```

Inserts an item with its precepts to the transaction

#### Arguments:
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

#### Raises:
    Exception: Raises with an error message of API return if Transaction is over
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.update"></a>

### update

```python
def update(item_def, precepts=None)
```

Updates an item with its precepts to the transaction

#### Arguments:
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

#### Raises:
    Exception: Raises with an error message of API return if Transaction is over
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.upsert"></a>

### upsert

```python
def upsert(item_def, precepts=None)
```

Updates an item with its precepts to the transaction. Creates the item if it not exists

#### Arguments:
    item_def (dict): A dictionary of item definition
    precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

#### Raises:
    Exception: Raises with an error message of API return if Transaction is over
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.delete"></a>

### delete

```python
def delete(item_def)
```

Deletes an item from the transaction

#### Arguments:
    item_def (dict): A dictionary of item definition

#### Raises:
    Exception: Raises with an error message of API return if Transaction is over
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.commit"></a>

### commit

```python
def commit()
```

Applies changes

#### Raises:
    Exception: Raises with an error message of API return if Transaction is over
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.commit_with_count"></a>

### commit\_with\_count

```python
def commit_with_count() -> int
```

Applies changes and return the number of count of changed items

#### Raises:
    Exception: Raises with an error message of API return if Transaction is over
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.transaction.Transaction.rollback"></a>

### rollback

```python
def rollback()
```

Rollbacks changes

#### Raises:
    Exception: Raises with an error message of API return if Transaction is over
    Exception: Raises with an error message of API return on non-zero error code

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
    root (:object:`Query`): The root query of the Reindexer query
    join_type (:enum:`JoinType`): Join type
    join_queries (list[:object:`Query`]): The list of join Reindexer query objects
    merged_queries (list[:object:`Query`]): The list of merged Reindexer query objects

<a id="pyreindexer.query.Query.where"></a>

### where

```python
def where(index: str,
          condition: CondType,
          keys: Union[simple_types, List[simple_types]] = None) -> Query
```

Adds where condition to DB query with args

#### Arguments:
    index (string): Field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    keys (Union[None, simple_types, list[simple_types]]):
        Value of index to be compared with. For composite indexes keys must be list, with value of each subindex

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.where_query"></a>

### where\_query

```python
def where_query(sub_query: Query,
                condition: CondType,
                keys: Union[simple_types, List[simple_types]] = None) -> Query
```

Adds sub-query where condition to DB query with args

#### Arguments:
    sub_query (:obj:`Query`): Field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    keys (Union[None, simple_types, list[simple_types]]):
        Value of index to be compared with. For composite indexes keys must be list, with value of each sub-index

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.where_composite"></a>

### where\_composite

```python
def where_composite(index: str, condition: CondType,
                    sub_query: Query) -> Query
```

Adds where condition to DB query with interface args for composite indexes

#### Arguments:
    index (string): Field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    sub_query (:obj:`Query`): Field name used in condition clause

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.where_uuid"></a>

### where\_uuid

```python
def where_uuid(index: str, condition: CondType, keys: List[str]) -> Query
```

Adds where condition to DB query with UUID as string args.
    This function applies binary encoding to the UUID value.
    `index` MUST be declared as uuid index in this case

#### Arguments:
    index (string): Field name used in condition clause
    condition (:enum:`CondType`): Type of condition
    keys (list[string]): Value of index to be compared with. For composite indexes keys must be list, with value of each subindex

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.where_between_fields"></a>

### where\_between\_fields

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

### open\_bracket

```python
def open_bracket() -> Query
```

Opens bracket for where condition to DB query

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.close_bracket"></a>

### close\_bracket

```python
def close_bracket() -> Query
```

Closes bracket for where condition to DB query

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.match"></a>

### match

```python
def match(index: str, keys: List[str]) -> Query
```

Adds string EQ-condition to DB query with string args

#### Arguments:
    index (string): Field name used in condition clause
    keys (list[string]): Value of index to be compared with. For composite indexes keys must be list, with value of each subindex

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.dwithin"></a>

### dwithin

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

### distinct

```python
def distinct(index: str) -> Query
```

Performs distinct for a certain index. Return only items with uniq value of field

#### Arguments:
    index (string): Field name for distinct operation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.aggregate_sum"></a>

### aggregate\_sum

```python
def aggregate_sum(index: str) -> Query
```

Performs a summation of values for a specified index

#### Arguments:
    index (string): Field name for sum operation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.aggregate_avg"></a>

### aggregate\_avg

```python
def aggregate_avg(index: str) -> Query
```

Finds for the average at the specified index

#### Arguments:
    index (string): Field name for sum operation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.aggregate_min"></a>

### aggregate\_min

```python
def aggregate_min(index: str) -> Query
```

Finds for the minimum at the specified index

#### Arguments:
    index (string): Field name for sum operation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.aggregate_max"></a>

### aggregate\_max

```python
def aggregate_max(index: str) -> Query
```

Finds for the maximum at the specified index

#### Arguments:
    index (string): Field name for sum operation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.aggregate_facet"></a>

### aggregate\_facet

```python
def aggregate_facet(fields: List[str]) -> Query._AggregateFacet
```

Gets fields facet value. Applicable to multiple data fields and the result of that could be sorted by any data
    column or `count` and cut off by offset and limit. In order to support this functionality this method
    returns AggregationFacetRequest which has methods sort, limit and offset

#### Arguments:
    fields (list[string]): Fields any data column name or `count`, fields should not be empty

#### Returns:
    (:obj:`_AggregateFacet`): Request object for further customizations

<a id="pyreindexer.query.Query.sort"></a>

### sort

```python
def sort(index: str,
         desc: bool = False,
         keys: Union[simple_types, List[simple_types]] = None) -> Query
```

Applies sort order to return from query items. If values argument specified, then items equal to values,
    if found will be placed in the top positions. Forced sort is support for the first sorting field only

#### Arguments:
    index (string): The index name
    desc (bool): Sort in descending order
    keys (Union[None, simple_types, List[simple_types]]):
        Value of index to match. For composite indexes keys must be list, with value of each sub-index

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.sort_stpoint_distance"></a>

### sort\_stpoint\_distance

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

### sort\_stfield\_distance

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
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.op_and"></a>

### op\_and

```python
def op_and() -> Query
```

Next condition will be added with AND.
    This is the default operation for WHERE statement. Do not have to be called explicitly in user's code.
    Used in DSL conversion

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.op_or"></a>

### op\_or

```python
def op_or() -> Query
```

Next condition will be added with OR.
    Implements short-circuiting:
    if the previous condition is successful the next will not be evaluated, but except Join conditions

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.op_not"></a>

### op\_not

```python
def op_not() -> Query
```

Next condition will be added with NOT AND.
    Implements short-circuiting: if the previous condition is failed the next will not be evaluated

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.request_total"></a>

### request\_total

```python
def request_total(total_name: str = '') -> Query
```

Requests total items calculation

#### Arguments:
    total_name (string, optional): Name to be requested

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.cached_total"></a>

### cached\_total

```python
def cached_total(total_name: str = '') -> Query
```

Requests cached total items calculation

#### Arguments:
    total_name (string, optional): Name to be requested

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.limit"></a>

### limit

```python
def limit(limit_items: int) -> Query
```

Sets a limit (count) of returned items. Analog to sql LIMIT rowsNumber

#### Arguments:
    limit_items (int): Number of rows to get from result set

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.offset"></a>

### offset

```python
def offset(start_offset: int) -> Query
```

Sets the number of the first selected row from result query

#### Arguments:
    limit_items (int): Index of the first row to get from result set

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.debug"></a>

### debug

```python
def debug(level: int) -> Query
```

Changes debug level

#### Arguments:
    level (int): Debug level

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.strict"></a>

### strict

```python
def strict(mode: StrictMode) -> Query
```

Changes strict mode

#### Arguments:
    mode (:enum:`StrictMode`): Strict mode

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.explain"></a>

### explain

```python
def explain() -> Query
```

Enables explain query

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.with_rank"></a>

### with\_rank

```python
def with_rank() -> Query
```

Outputs fulltext rank. Allowed only with fulltext query

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.execute"></a>

### execute

```python
def execute() -> QueryResults
```

Executes a select query

#### Returns:
    (:obj:`QueryResults`): A QueryResults iterator

#### Raises:
    Exception: Raises with an error message when query is in an invalid state
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.delete"></a>

### delete

```python
def delete() -> int
```

Executes a query, and delete items, matches query

#### Returns:
    (int): Number of deleted elements

#### Raises:
    Exception: Raises with an error message when query is in an invalid state
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.set_object"></a>

### set\_object

```python
def set_object(field: str, values: List[simple_types]) -> Query
```

Adds an update query to an object field for an update query

#### Arguments:
    field (string): Field name
    values (list[simple_types]): List of values to add

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.set"></a>

### set

```python
def set(field: str, values: List[simple_types]) -> Query
```

Adds a field update request to the update request

#### Arguments:
    field (string): Field name
    values (list[simple_types]): List of values to add

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.drop"></a>

### drop

```python
def drop(index: str) -> Query
```

Drops a value for a field

#### Arguments:
    index (string): Field name for drop operation

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.expression"></a>

### expression

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

### update

```python
def update() -> QueryResults
```

Executes update query, and update fields in items, which matches query

#### Returns:
    (:obj:`QueryResults`): A QueryResults iterator

#### Raises:
    Exception: Raises with an error message when query is in an invalid state
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.must_execute"></a>

### must\_execute

```python
def must_execute() -> QueryResults
```

Executes a query, and update fields in items, which matches query, with status check

#### Returns:
    (:obj:`QueryResults`): A QueryResults iterator

#### Raises:
    Exception: Raises with an error message when query is in an invalid state
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.get"></a>

### get

```python
def get() -> (str, bool)
```

Executes a query, and return 1 JSON item

#### Returns:
    (:tuple:string,bool): 1st string item and found flag

#### Raises:
    Exception: Raises with an error message when query is in an invalid state
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.inner_join"></a>

### inner\_join

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

### join

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

### left\_join

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

### merge

```python
def merge(query: Query) -> Query
```

Merges queries of the same type

#### Arguments:
    query (:obj:`Query`): Query object to merge

#### Returns:
    (:obj:`Query`): Query object for further customizations

<a id="pyreindexer.query.Query.on"></a>

### on

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

<a id="pyreindexer.query.Query.select"></a>

### select

```python
def select(fields: List[str]) -> Query
```

Sets list of columns in this namespace to be finally selected.
    The columns should be specified in the same case as the jsonpaths corresponding to them.
    Non-existent fields and fields in the wrong case are ignored.
    If there are no fields in this list that meet these conditions, then the filter works as "*"

#### Arguments:
    fields (list[string]): List of columns to be selected

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.functions"></a>

### functions

```python
def functions(functions: List[str]) -> Query
```

Adds sql-functions to query

#### Arguments:
    functions (list[string]): Functions declaration

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    Exception: Raises with an error message of API return on non-zero error code

<a id="pyreindexer.query.Query.equal_position"></a>

### equal\_position

```python
def equal_position(equal_position: List[str]) -> Query
```

Adds equal position fields to arrays queries

#### Arguments:
    equal_poses (list[string]): Equal position fields to arrays queries

#### Returns:
    (:obj:`Query`): Query object for further customizations

#### Raises:
    Exception: Raises with an error message of API return on non-zero error code

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


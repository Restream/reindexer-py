from __future__ import annotations

from typing import Dict, List

from pyreindexer.query import Query
from pyreindexer.query_results import QueryResults
from pyreindexer.raiser_mixin import RaiserMixin, raise_if_error
from pyreindexer.transaction import Transaction


class RxConnector(RaiserMixin):
    """RxConnector provides a binding to Reindexer upon two shared libraries (hereinafter - APIs): 'rawpyreindexerb.so'
        and 'rawpyreindexerc.so'. The first one is aimed to a builtin way usage. That API embeds Reindexer, so it could
        be used right in-place as is. The second one acts as a lightweight client which establishes a connection to
        Reindexer server via RPC. The APIs interfaces are completely the same.

    #### Attributes:
        api (module): An API module loaded dynamically for Reindexer calls
        rx (int): A memory pointer to Reindexer instance
        err_code (int): The API error code
        err_msg (string): The API error message

    """

    def __init__(self, dsn: str, *,
                 # cproto options
                 fetch_amount: int = 1000,
                 connect_timeout: int = 0,
                 request_timeout: int = 0,
                 enable_compression: bool = False,
                 start_special_thread: bool = False,
                 client_name: str = 'pyreindexer',
                 # builtin options
                 max_replication_updates_size: int = 1024 * 1024 * 1024,
                 allocator_cache_limit: int = -1,
                 allocator_cache_part: float = -1.0):
        """Constructs a new connector object.
        Initializes an error code and a Reindexer instance descriptor to zero

        #### Arguments:
            dsn (string): The connection string which contains a protocol
                Examples: 'builtin:///tmp/pyrx', 'cproto://127.0.0.1:6534/pyrx'

            cproto options:
                 fetch_amount (int): The number of items that will be fetched by one operation
                 connect_timeout (int): Connection and database login timeout value [seconds]
                 request_timeout (int): Request execution timeout value [seconds]
                 enable_compression (bool): Flag enable/disable traffic compression
                 start_special_thread (bool): Determines whether to request a special thread of execution
                    on the server for this connection
                 client_name (string): Proper name of the application (as a client for Reindexer-server)

            built-in options:
                max_replication_updates_size (int): Max pended replication updates size in bytes
                allocator_cache_limit (int): Recommended maximum free cache size of tcmalloc memory allocator in bytes
                allocator_cache_part (float): Recommended maximum free cache size of tcmalloc memory allocator in
                    relation to total reindexer allocated memory size, in units

        """

        self.err_code: int = 0
        self.err_msg: str = ''
        self.rx = 0
        self._api_import(dsn)
        self.rx = self.api.init(fetch_amount, connect_timeout, request_timeout, enable_compression,
                                start_special_thread, client_name, max_replication_updates_size,
                                allocator_cache_limit, allocator_cache_part)
        self._api_connect(dsn)

    def __del__(self):
        """Closes an API instance on a connector object deletion if the API is initialized

        """

        if self.rx > 0:
            self._api_close()

    def close(self) -> None:
        """Closes an API instance with Reindexer resources freeing

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet

        """

        self._api_close()

    @raise_if_error
    def namespace_open(self, namespace: str) -> None:
        """Opens a namespace specified or creates a namespace if it does not exist

        #### Arguments:
            namespace (string): A name of a namespace

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.namespace_open(self.rx, namespace)

    @raise_if_error
    def namespace_close(self, namespace: str) -> None:
        """Closes a namespace specified

        #### Arguments:
            namespace (string): A name of a namespace

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.namespace_close(self.rx, namespace)

    @raise_if_error
    def namespace_drop(self, namespace: str) -> None:
        """Drops a namespace specified

        #### Arguments:
            namespace (string): A name of a namespace

        #### Raises:
            Exception: Raises with an error message when Reindexer instance is not initialized yet
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.namespace_drop(self.rx, namespace)

    @raise_if_error
    def namespaces_enum(self, enum_not_opened: bool = False) -> List[Dict[str, str]]:
        """Gets a list of namespaces available

        #### Arguments:
            enum_not_opened (bool, optional): An enumeration mode flag. If it is
                set then closed namespaces are in result list too. Defaults to False

        #### Returns:
            (:obj:`list` of :obj:`dict`): A list of dictionaries which describe each namespace

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg, res = self.api.namespaces_enum(self.rx, enum_not_opened)
        return res

    @raise_if_error
    def index_add(self, namespace: str, index_def: Dict) -> None:
        """Adds an index to the namespace specified

        #### Arguments:
            namespace (string): A name of a namespace
            index_def (dict): A dictionary of index definition

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.index_add(self.rx, namespace, index_def)

    @raise_if_error
    def index_update(self, namespace: str, index_def: Dict) -> None:
        """Updates an index in the namespace specified

        #### Arguments:
            namespace (string): A name of a namespace
            index_def (dict): A dictionary of index definition

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.index_update(self.rx, namespace, index_def)

    @raise_if_error
    def index_drop(self, namespace: str, index_name: Dict) -> None:
        """Drops an index from the namespace specified

        #### Arguments:
            namespace (string): A name of a namespace
            index_name (string): A name of an index

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.index_drop(self.rx, namespace, index_name)

    @raise_if_error
    def item_insert(self, namespace: str, item_def: Dict, precepts: List[str] = None) -> None:
        """Inserts an item with its precepts to the namespace specified

        #### Arguments:
            namespace (string): A name of a namespace
            item_def (dict): A dictionary of item definition
            precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        precepts = [] if precepts is None else precepts
        self.err_code, self.err_msg = self.api.item_insert(self.rx, namespace, item_def, precepts)

    @raise_if_error
    def item_update(self, namespace: str, item_def: Dict, precepts: List[str] = None) -> None:
        """Updates an item with its precepts in the namespace specified

        #### Arguments:
            namespace (string): A name of a namespace
            item_def (dict): A dictionary of item definition
            precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        precepts = [] if precepts is None else precepts
        self.err_code, self.err_msg = self.api.item_update(self.rx, namespace, item_def, precepts)

    @raise_if_error
    def item_upsert(self, namespace: str, item_def: Dict, precepts: List[str] = None) -> None:
        """Updates an item with its precepts in the namespace specified. Creates the item if it not exists

        #### Arguments:
            namespace (string): A name of a namespace
            item_def (dict): A dictionary of item definition
            precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        precepts = [] if precepts is None else precepts
        self.err_code, self.err_msg = self.api.item_upsert(self.rx, namespace, item_def, precepts)

    @raise_if_error
    def item_delete(self, namespace: str, item_def: Dict) -> None:
        """Deletes an item from the namespace specified

        #### Arguments:
            namespace (string): A name of a namespace
            item_def (dict): A dictionary of item definition

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.item_delete(self.rx, namespace, item_def)

    @raise_if_error
    def meta_put(self, namespace: str, key: str, value: str) -> None:
        """Puts metadata to a storage of Reindexer by key

        #### Arguments:
            namespace (string): A name of a namespace
            key (string): A key in a storage of Reindexer for metadata keeping
            value (string): A metadata for storage

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.meta_put(self.rx, namespace, key, value)

    @raise_if_error
    def meta_get(self, namespace: str, key: str) -> str:
        """Gets metadata from a storage of Reindexer by key specified

        #### Arguments:
            namespace (string): A name of a namespace
            key (string): A key in a storage of Reindexer where metadata is kept

        #### Returns:
            string: A metadata value

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg, res = self.api.meta_get(self.rx, namespace, key)
        return res

    @raise_if_error
    def meta_delete(self, namespace: str, key: str) -> None:
        """Deletes metadata from a storage of Reindexer by key specified

        #### Arguments:
            namespace (string): A name of a namespace
            key (string): A key in a storage of Reindexer where metadata is kept

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.meta_delete(self.rx, namespace, key)

    @raise_if_error
    def meta_enum(self, namespace: str) -> List[str]:
        """Gets a list of metadata keys from a storage of Reindexer

        #### Arguments:
            namespace (string): A name of a namespace

        #### Returns:
            (:obj:`list` of :obj:`str`): A list of all metadata keys

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg, res = self.api.meta_enum(self.rx, namespace)
        return res

    @raise_if_error
    def select(self, query: str) -> QueryResults:
        """Executes an SQL query and returns query results

        #### Arguments:
            query (string): An SQL query

        #### Returns:
            (:obj:`QueryResults`): A QueryResults iterator

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg, wrapper_ptr, iter_count, total_count = self.api.select(self.rx, query)
        return QueryResults(self.api, wrapper_ptr, iter_count, total_count)

    @raise_if_error
    def new_transaction(self, namespace: str) -> Transaction:
        """Starts a new transaction and return the transaction object to processing

        #### Arguments:
            namespace (string): A name of a namespace

        #### Returns:
            (:obj:`Transaction`): A new transaction

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg, transaction_wrapper_ptr = self.api.new_transaction(self.rx, namespace)
        return Transaction(self.api, transaction_wrapper_ptr)

    @raise_if_error
    def new_query(self, namespace: str) -> Query:
        """Creates a new query and return the query object to processing

        #### Arguments:
            namespace (string): A name of a namespace

        #### Returns:
            (:obj:`Query`): A new query

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet

        """

        self.err_code, self.err_msg, query_wrapper_ptr = self.api.create_query(self.rx, namespace)
        return Query(self.api, query_wrapper_ptr)

    def with_timeout(self, timeout: int) -> RxConnector:
        """Add execution timeout to the next query

        #### Arguments:
            timeout (int): Optional server-side execution timeout for each subquery [milliseconds]

        #### Returns:
            (:obj:`RxConnector`): RxConnector object for further customizations

        """

        self.api.with_timeout(self.rx, timeout)
        return self

    def _api_import(self, dsn: str) -> None:
        """Imports an API dynamically depending on protocol specified in dsn

        #### Arguments:
            dsn (string): The connection string which contains a protocol

        #### Raises:
            ConnectionError: Raises an exception if a connection protocol is unrecognized

        """

        if dsn.startswith('builtin://'):
            self.api = __import__('rawpyreindexerb')
        elif dsn.startswith('cproto://'):
            self.api = __import__('rawpyreindexerc')
        else:
            raise ConnectionError(f"Unknown Reindexer connection protocol for dsn: {dsn}")

    def _api_connect(self, dsn: str) -> None:
        """Connects to a database specified in dsn. Obtains a pointer to Reindexer instance

        #### Arguments:
            dsn (string): The connection string which contains a protocol

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.raise_on_not_init()
        self.err_code, self.err_msg = self.api.connect(self.rx, dsn)
        self.raise_on_error()

    def _api_close(self) -> None:
        """Destructs Reindexer instance correctly and resets memory pointer

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet

        """

        self.raise_on_not_init()
        self.api.destroy(self.rx)
        self.rx = 0

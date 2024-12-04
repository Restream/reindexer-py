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

    def __init__(self, dsn):
        """Constructs a new connector object.
        Initializes an error code and a Reindexer instance descriptor to zero

        #### Arguments:
            dsn (string): The connection string which contains a protocol
            Examples: 'builtin:///tmp/pyrx', 'cproto://127.0.0.1:6534/pyrx'

        """

        self.err_code = 0
        self.err_msg = ''
        self.rx = 0
        self._api_import(dsn)
        self._api_init(dsn)

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
    def namespace_open(self, namespace) -> None:
        """Opens a namespace specified or creates a namespace if it does not exist

        #### Arguments:
            namespace (string): A name of a namespace

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.namespace_open(self.rx, namespace)

    @raise_if_error
    def namespace_close(self, namespace) -> None:
        """Closes a namespace specified

        #### Arguments:
            namespace (string): A name of a namespace

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.namespace_close(self.rx, namespace)

    @raise_if_error
    def namespace_drop(self, namespace) -> None:
        """Drops a namespace specified

        #### Arguments:
            namespace (string): A name of a namespace

        #### Raises:
            Exception: Raises with an error message when Reindexer instance is not initialized yet
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.namespace_drop(self.rx, namespace)

    @raise_if_error
    def namespaces_enum(self, enum_not_opened=False) -> List[Dict[str, str]]:
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
    def index_add(self, namespace, index_def) -> None:
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
    def index_update(self, namespace, index_def) -> None:
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
    def index_drop(self, namespace, index_name) -> None:
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
    def item_insert(self, namespace, item_def, precepts=None) -> None:
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
    def item_update(self, namespace, item_def, precepts=None) -> None:
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
    def item_upsert(self, namespace, item_def, precepts=None) -> None:
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
    def item_delete(self, namespace, item_def) -> None:
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
    def meta_put(self, namespace, key, value) -> None:
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
    def meta_get(self, namespace, key) -> str:
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
    def meta_delete(self, namespace, key) -> None:
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
    def meta_enum(self, namespace) -> List[str]:
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
    def new_transaction(self, namespace) -> Transaction:
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

    def _api_import(self, dsn):
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

    def _api_init(self, dsn):
        """Initializes Reindexer instance and connects to a database specified in dsn
        Obtains a pointer to Reindexer instance

        #### Arguments:
            dsn (string): The connection string which contains a protocol

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.rx = self.api.init()
        self.raise_on_not_init()
        self.err_code, self.err_msg = self.api.connect(self.rx, dsn)
        self.raise_on_error()

    def _api_close(self):
        """Destructs Reindexer instance correctly and resets memory pointer

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet

        """

        self.raise_on_not_init()
        self.api.destroy(self.rx)
        self.rx = 0

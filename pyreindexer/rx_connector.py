from __future__ import annotations

import json
import queue
import threading
from datetime import timedelta
from typing import Dict, List, Optional, Union

from pyreindexer.index_definition import IndexDefinition
from pyreindexer.query import Query
from pyreindexer.query_results import QueryResults
from pyreindexer.raiser_mixin import RaiserRx
from pyreindexer.transaction import Transaction


class RxConnector(RaiserRx):
    """RxConnector provides a binding to Reindexer upon two shared libraries (hereinafter - APIs): 'rawpyreindexerb.so'
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

    """

    def __init__(self, dsn: str, *,
                 # cproto options
                 fetch_amount: int = 1000,
                 reconnect_attempts: int = 0,
                 net_timeout: timedelta = timedelta(milliseconds=0),
                 enable_compression: bool = False,
                 start_special_thread: bool = False,
                 client_name: str = 'pyreindexer',
                 sync_rxcoro_count: int = 10,
                 # builtin options
                 max_replication_updates_size: int = 1024 * 1024 * 1024,
                 allocator_cache_limit: int = -1,
                 allocator_cache_part: float = -1.0):
        """Constructs a new connector object.

        #### Arguments:
            dsn (string): The connection string which contains a protocol
                Examples: 'builtin:///tmp/pyrx', 'cproto://127.0.0.1:6534/pyrx'

            cproto options:
                 fetch_amount (int): The number of items that will be fetched by one operation (must be > 0)
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

        #### Raises:
            ValueError: Raises with an error message when input value is invalid

        """

        self.err_code: int = 0
        self.err_msg: str = ''
        self.rx: int = 0

        # Ownership ledger of native wrappers. Mutation only under _wrappers_lock.
        # Query/Transaction.__del__ must not touch these sets, this lock, or C:
        # GC can run during set.add. It only enqueues the stolen ptr. Queries are
        # reaped on new_query()/close(); transactions on new_transaction()/commit/
        # rollback/close().
        # close() is not safe to call while other threads still use this connector.
        self._query_ptrs = set()
        self._tx_ptrs = set()
        self._query_gc_queue: queue.SimpleQueue = queue.SimpleQueue()
        self._tx_gc_queue: queue.SimpleQueue = queue.SimpleQueue()
        self._wrappers_lock = threading.Lock()

        if fetch_amount <= 0:
            raise ValueError("'fetch_amount' must be greater than zero")

        self._api_import(dsn)
        milliseconds: int = int(net_timeout / timedelta(milliseconds=1))
        self.rx = self.api.init(fetch_amount, reconnect_attempts, milliseconds, enable_compression,
                                start_special_thread, client_name, sync_rxcoro_count,
                                max_replication_updates_size, allocator_cache_limit, allocator_cache_part)
        self._api_connect(dsn, net_timeout)

    def __del__(self):
        """Closes the API instance upon connector object deletion if the API is initialized

        """

        try:
            self._shutdown_wrappers_and_db(suppress=True)
        except Exception:
            pass

    @staticmethod
    def _check_index_fields(index: dict):
        required_fields = ("name", "json_paths", "field_type", "index_type")
        for field in required_fields:
            if field not in index:
                raise AttributeError(f"Index must contain field '{field}'")
        if index["field_type"] == "float_vector":
            if not index.get("config"):
                raise AttributeError(f"Vector index must contain nonempty 'config'")

    def _api_import(self, dsn: str) -> None:
        """Imports an API dynamically depending on protocol specified in dsn

        #### Arguments:
            dsn (string): The connection string which contains a protocol

        #### Raises:
            ConnectionError: Raises an exception if a connection protocol is unrecognized

        """

        if dsn.startswith('builtin://'):
            self.api = __import__('rawpyreindexerb')
        elif dsn.startswith(('cproto://', 'cprotos://', 'ucproto://')):
            self.api = __import__('rawpyreindexerc')
        else:
            raise ConnectionError(f"Unknown Reindexer connection protocol for dsn: {dsn}")

    def _api_connect(self, dsn: str, timeout: timedelta) -> None:
        """Connects to a database specified in dsn. Obtains a pointer to Reindexer instance

        #### Arguments:
            dsn (string): The connection string which contains a protocol
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.raise_on_not_init()
        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg = self.api.connect(self.rx, dsn, milliseconds)
        self.raise_on_error()

    def _api_close(self) -> None:
        """Destructs Reindexer instance correctly and resets memory pointer

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet

        """

        self.raise_on_not_init()
        self.api.destroy(self.rx)
        self.rx = 0

    def close(self) -> None:
        """Closes the API instance and frees Reindexer resources.
            Also rolls back leftover transactions and destroys leftover queries
            that were not finished yet.
            Do not call `close()` while other threads still use this connector
            (`execute`, item operations, transactions, `new_query`, and so on).

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet

        """

        self._shutdown_wrappers_and_db(suppress=False)

    def _take_queued_locked(self, gc_queue: queue.SimpleQueue, ledger: set) -> list:
        """Move queued ptrs out of the ledger. Caller holds _wrappers_lock."""

        taken = []
        while True:
            try:
                ptr = gc_queue.get_nowait()
            except queue.Empty:
                break
            try:
                ledger.remove(ptr)
            except KeyError:
                continue
            taken.append(ptr)
        return taken

    def _take_queued_txs_locked(self) -> list:
        return self._take_queued_locked(self._tx_gc_queue, self._tx_ptrs)

    def _take_queued_queries_locked(self) -> list:
        return self._take_queued_locked(self._query_gc_queue, self._query_ptrs)

    def _pop_all_txs_locked(self) -> list:
        ptrs = self._take_queued_txs_locked()
        leftover = list(self._tx_ptrs)
        self._tx_ptrs.clear()
        ptrs.extend(leftover)
        return ptrs

    def _pop_all_queries_locked(self) -> list:
        ptrs = self._take_queued_queries_locked()
        leftover = list(self._query_ptrs)
        self._query_ptrs.clear()
        ptrs.extend(leftover)
        return ptrs

    def _rollback_native_txs(self, ptrs: list) -> Optional[BaseException]:
        api = getattr(self, 'api', None)
        first_err: Optional[BaseException] = None
        for ptr in ptrs:
            if api is None:
                continue
            try:
                api.transaction_rollback(ptr, 0)
            except Exception as e:
                if first_err is None:
                    first_err = e
        return first_err

    def _destroy_native_queries(self, ptrs: list) -> Optional[BaseException]:
        api = getattr(self, 'api', None)
        first_err: Optional[BaseException] = None
        for ptr in ptrs:
            if api is None:
                continue
            try:
                api.destroy_query(ptr)
            except Exception as e:
                if first_err is None:
                    first_err = e
        return first_err

    def _reap_queries_locked(self) -> None:
        """Destroys queued query wrappers. Caller must hold _wrappers_lock.

        destroy_query does not release the GIL, so it is safe (and short) under the lock.
        """

        self._destroy_native_queries(self._take_queued_queries_locked())

    def _shutdown_wrappers_and_db(self, *, suppress: bool) -> None:
        """Destroys leftover Query/Tx wrappers, then the Reindexer instance."""

        lock = getattr(self, '_wrappers_lock', None)
        if lock is None:
            return
        first_err: Optional[BaseException] = None
        with lock:
            if self.rx <= 0:
                if not suppress:
                    self.raise_on_not_init()
                return
            tx_ptrs = self._pop_all_txs_locked()
            query_ptrs = self._pop_all_queries_locked()

        tx_err = self._rollback_native_txs(tx_ptrs)
        query_err = self._destroy_native_queries(query_ptrs)

        with lock:
            if self.rx > 0:
                try:
                    self._api_close()
                except Exception as e:
                    first_err = e

        if suppress:
            return
        for err in (tx_err, query_err, first_err):
            if err is not None:
                raise err

    @RaiserRx.raise_if_error
    def namespace_open(self, namespace: str, timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Opens the specified namespace or creates it if it does not exist

        #### Arguments:
            namespace (string): The name of the namespace
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg = self.api.namespace_open(self.rx, namespace, milliseconds)

    @RaiserRx.raise_if_error
    def namespace_close(self, namespace: str, timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Closes the specified namespace

        #### Arguments:
            namespace (string): The name of the namespace
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg = self.api.namespace_close(self.rx, namespace, milliseconds)

    @RaiserRx.raise_if_error
    def namespace_drop(self, namespace: str, timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Drops the specified namespace

        #### Arguments:
            namespace (string): The name of the namespace
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            Exception: Raises with an error message when Reindexer instance is not initialized yet
            Exception: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg = self.api.namespace_drop(self.rx, namespace, milliseconds)

    @RaiserRx.raise_if_error
    def namespace_truncate(self, namespace: str, timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Truncates the specified namespace

        #### Arguments:
            namespace (string): The name of the namespace
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            Exception: Raises with an error message when Reindexer instance is not initialized yet
            Exception: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg = self.api.namespace_truncate(self.rx, namespace, milliseconds)

    @RaiserRx.raise_if_error
    def namespace_rename(self, old_ns_name: str, new_ns_name: str,
                         timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Renames the specified namespace

        #### Arguments:
            old_ns_name (string): Old name of the namespace
            new_ns_name (string): New name of the namespace
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg = self.api.namespace_rename(self.rx, old_ns_name, new_ns_name, milliseconds)

    @RaiserRx.raise_if_error
    def namespaces_enum(self, enum_not_opened: bool = False,
                        timeout: timedelta = timedelta(milliseconds=0)) -> List[Dict[str, str]]:
        """Gets a list of available namespaces

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

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg, res = self.api.namespaces_enum(self.rx, enum_not_opened, milliseconds)
        return res

    @RaiserRx.raise_if_error
    def schema_set(self, namespace: str, schema: Dict, timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Sets the schema for the specified namespace

        #### Arguments:
            namespace (string): The name of the namespace
            schema (dict): Schema definition
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        schema = json.dumps(schema)
        self.err_code, self.err_msg = self.api.schema_set(self.rx, namespace, schema, milliseconds)

    @RaiserRx.raise_if_error
    def index_add(self, namespace: str, index_def: Union[IndexDefinition, Dict],
                  timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Adds an index to the specified namespace

        #### Arguments:
            namespace (string): The name of the namespace
            index_def (Union[IndexDefinition, dict]): IndexDefinition object | dict with index definition
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        if isinstance(index_def, IndexDefinition):
            index_def = index_def.to_dict()
        self._check_index_fields(index_def)
        self.err_code, self.err_msg = self.api.index_add(self.rx, namespace, index_def, milliseconds)

    @RaiserRx.raise_if_error
    def index_update(self, namespace: str, index_def: Union[IndexDefinition, Dict],
                     timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Updates an index in the specified namespace

        #### Arguments:
            namespace (string): The name of the namespace
            index_def (Union[IndexDefinition, dict]): IndexDefinition object | dict with index definition
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        if isinstance(index_def, IndexDefinition):
            index_def = index_def.to_dict()
        self._check_index_fields(index_def)
        self.err_code, self.err_msg = self.api.index_update(self.rx, namespace, index_def, milliseconds)

    @RaiserRx.raise_if_error
    def index_drop(self, namespace: str, index_name: str, timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Drops an index from the specified namespace

        #### Arguments:
            namespace (string): The name of the namespace
            index_name (string): A name of an index
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg = self.api.index_drop(self.rx, namespace, index_name, milliseconds)

    @RaiserRx.raise_if_error
    def item_insert(self, namespace: str, item_def: Dict, precepts: List[str] = None,
                    timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Inserts an item with its precepts into the specified namespace

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

        """

        precepts = [] if precepts is None else precepts
        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg = self.api.item_insert(self.rx, namespace, item_def, precepts, milliseconds)

    @RaiserRx.raise_if_error
    def item_update(self, namespace: str, item_def: Dict, precepts: List[str] = None,
                    timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Updates an item with its precepts in the specified namespace

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

        """

        precepts = [] if precepts is None else precepts
        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg = self.api.item_update(self.rx, namespace, item_def, precepts, milliseconds)

    @RaiserRx.raise_if_error
    def item_upsert(self, namespace: str, item_def: Dict, precepts: List[str] = None,
                    timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Updates an item with its precepts in the specified namespace. Creates the item if it does not exist

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

        """

        precepts = [] if precepts is None else precepts
        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg = self.api.item_upsert(self.rx, namespace, item_def, precepts, milliseconds)

    @RaiserRx.raise_if_error
    def item_delete(self, namespace: str, item_def: Dict, timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Deletes an item from the namespace specified

        #### Arguments:
            namespace (string): The name of the namespace
            item_def (dict): A dictionary of item definition
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg = self.api.item_delete(self.rx, namespace, item_def, [], milliseconds)

    @RaiserRx.raise_if_error
    def meta_put(self, namespace: str, key: str, value: str, timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Puts metadata into the Reindexer storage for the specified key

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

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg = self.api.meta_put(self.rx, namespace, key, value, milliseconds)

    @RaiserRx.raise_if_error
    def meta_get(self, namespace: str, key: str, timeout: timedelta = timedelta(milliseconds=0)) -> str:
        """Gets metadata from the Reindexer storage by the specified key

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

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg, res = self.api.meta_get(self.rx, namespace, key, milliseconds)
        return res

    @RaiserRx.raise_if_error
    def meta_delete(self, namespace: str, key: str, timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Deletes metadata from the Reindexer storage by the specified key

        #### Arguments:
            namespace (string): The name of the namespace
            key (string): A key in a storage of Reindexer where metadata is kept
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet
            ApiError: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg = self.api.meta_delete(self.rx, namespace, key, milliseconds)

    @RaiserRx.raise_if_error
    def meta_enum(self, namespace: str, timeout: timedelta = timedelta(milliseconds=0)) -> List[str]:
        """Gets a list of metadata keys from the Reindexer storage

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

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg, res = self.api.meta_enum(self.rx, namespace, milliseconds)
        return res

    @RaiserRx.raise_if_error
    def exec_sql(self, query: str, timeout: timedelta = timedelta(milliseconds=0)) -> QueryResults:
        """Executes an SQL query and returns query results

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

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg, wrapper_ptr, iter_count, total_count = self.api.exec_sql(self.rx, query,
                                                                                              milliseconds)
        return QueryResults(self.api, wrapper_ptr, iter_count, total_count)

    @RaiserRx.raise_if_error
    def new_transaction(self, namespace: str, timeout: timedelta = timedelta(milliseconds=0)) -> Transaction:
        """Starts a new transaction and returns the transaction object.
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

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        with self._wrappers_lock:
            self.raise_on_not_init()
            queued_txs = self._take_queued_txs_locked()
        self._rollback_native_txs(queued_txs)
        self.err_code, self.err_msg, transaction_wrapper_ptr = self.api.new_transaction(
            self.rx, namespace, milliseconds)
        with self._wrappers_lock:
            if transaction_wrapper_ptr > 0:
                self._tx_ptrs.add(transaction_wrapper_ptr)
        return Transaction(self, transaction_wrapper_ptr)

    @RaiserRx.raise_if_error
    def new_query(self, namespace: str) -> Query:
        """Creates a new query and returns the query object.
            Also frees native resources of Query objects dropped since the previous
            `new_query()` or `close()`.

        #### Arguments:
            namespace (string): The name of the namespace

        #### Returns:
            (:obj:`Query`): A new query

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet

        """

        with self._wrappers_lock:
            self.raise_on_not_init()
            self._reap_queries_locked()
            self.err_code, self.err_msg, query_wrapper_ptr = self.api.create_query(self.rx, namespace)
            if query_wrapper_ptr > 0:
                self._query_ptrs.add(query_wrapper_ptr)
            return Query(self, query_wrapper_ptr)

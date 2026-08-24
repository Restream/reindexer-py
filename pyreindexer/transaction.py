from datetime import timedelta
from typing import Dict, List

from pyreindexer.exceptions import TransactionError
from pyreindexer.query import Query
from pyreindexer.raiser_mixin import RaiserTx


class Transaction(RaiserTx):
    """An object representing the context of a Reindexer transaction

    Call `commit()` or `rollback()` explicitly to finish a transaction.
        Dropping the object without that is only a safety net: rollback may be
        deferred until the next `RxConnector.new_transaction()` or `RxConnector.close()`.

    #### Attributes:
        api (module): An API module for Reindexer calls
        transaction_wrapper_ptr (int): A memory pointer to Reindexer transaction object
        err_code (int): The API error code
        err_msg (string): The API error message

    """

    def __init__(self, rx, transaction_wrapper_ptr: int):
        """Constructs a new Reindexer transaction object

        #### Arguments:
            api (module): An API module for Reindexer calls
            transaction_wrapper_ptr (int): A memory pointer to Reindexer transaction object

        """

        self.rx = rx
        self.api = rx.api
        self._owned_ptr = [transaction_wrapper_ptr]
        self.err_code: int = 0
        self.err_msg: str = ""

    @property
    def transaction_wrapper_ptr(self) -> int:
        try:
            return self._owned_ptr[0]
        except (AttributeError, IndexError):
            return 0

    def _steal_owned_ptr(self) -> int:
        try:
            return self._owned_ptr.pop()
        except (AttributeError, IndexError):
            return 0

    def __del__(self):
        """Enqueues an uncommitted transaction for later rollback.

        Actual rollback runs on the next new_transaction() or close() call.
        Callers should commit() or rollback() explicitly rather than relying on GC.

        """

        try:
            ptr = self._steal_owned_ptr()
            if ptr <= 0:
                return
            rx = getattr(self, 'rx', None)
            if rx is None:
                return
            rx._tx_gc_queue.put(ptr)
        except Exception:
            pass

    def _claim_locked(self) -> int:
        """Steal the wrapper ptr and drop it from the ledger. Caller holds _wrappers_lock."""

        ptr = self._steal_owned_ptr()
        if ptr > 0:
            self.rx._tx_ptrs.discard(ptr)
        return ptr

    def _finish_native(self, call):
        """Claim ownership, then commit/rollback without holding _wrappers_lock."""

        rx = self.rx
        with rx._wrappers_lock:
            rx.raise_on_not_init()
            ptr = self._claim_locked()
            if ptr <= 0:
                raise TransactionError("Transaction is over")
        try:
            return call(ptr)
        finally:
            with rx._wrappers_lock:
                extra_txs = rx._take_queued_txs_locked()
            rx._rollback_native_txs(extra_txs)

    @RaiserTx.raise_if_error
    def insert(self, item_def: Dict, precepts: List[str] = None) -> None:
        """Inserts an item with its precepts to the transaction
            Warning: the timeout set when the transaction was created is used

        #### Arguments:
            item_def (dict): A dictionary of item definition
            precepts (:obj:`list` of :obj:`str`): A list of strings representing precepts

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        precepts = [] if precepts is None else precepts
        self.err_code, self.err_msg = self.api.transaction_item_insert(self.transaction_wrapper_ptr, item_def, precepts)

    @RaiserTx.raise_if_error
    def update(self, item_def: Dict, precepts: List[str] = None) -> None:
        """Updates an item with its precepts to the transaction
            Warning: the timeout set when the transaction was created is used

        #### Arguments:
            item_def (dict): A dictionary of item definition
            precepts (:obj:`list` of :obj:`str`): A list of strings representing precepts

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        precepts = [] if precepts is None else precepts
        self.err_code, self.err_msg = self.api.transaction_item_update(self.transaction_wrapper_ptr, item_def, precepts)

    @RaiserTx.raise_if_error
    def update_query(self, query: Query) -> None:
        """Updates items with the transaction
            Read-committed isolation is available for read operations.
            Changes made in an active transaction are invisible to the other transactions.

        #### Arguments:
            query (:obj:`Query`): A query object to modify

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.transaction_modify(self.transaction_wrapper_ptr, query.query_wrapper_ptr)

    @RaiserTx.raise_if_error
    def upsert(self, item_def: Dict, precepts: List[str] = None) -> None:
        """Updates an item with its precepts to the transaction. Creates the item if it does not exist
            Warning: the timeout set when the transaction was created is used

        #### Arguments:
            item_def (dict): A dictionary of item definition
            precepts (:obj:`list` of :obj:`str`): A list of strings representing precepts

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        precepts = [] if precepts is None else precepts
        self.err_code, self.err_msg = self.api.transaction_item_upsert(self.transaction_wrapper_ptr, item_def, precepts)

    @RaiserTx.raise_if_error
    def delete(self, item_def: Dict) -> None:
        """Deletes an item from the transaction
            Warning: the timeout set when the transaction was created is used

        #### Arguments:
            item_def (dict): A dictionary of item definition

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.transaction_item_delete(self.transaction_wrapper_ptr, item_def)

    @RaiserTx.raise_if_error
    def delete_query(self, query: Query):
        """Deletes items with the transaction
            Read-committed isolation is available for read operations.
            Changes made in an active transaction are invisible to the other transactions.

        #### Arguments:
            query (:obj:`Query`): A query object to modify

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.transaction_delete(self.transaction_wrapper_ptr, query.query_wrapper_ptr)

    @RaiserTx.raise_if_error
    def commit(self, timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Applies changes and finishes the transaction

        #### Arguments:
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg, _ = self._finish_native(
            lambda ptr: self.api.transaction_commit(ptr, milliseconds))

    @RaiserTx.raise_if_error
    def commit_with_count(self, timeout: timedelta = timedelta(milliseconds=0)) -> int:
        """Applies changes, finishes the transaction and returns the number of changed items

        #### Arguments:
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg, count = self._finish_native(
            lambda ptr: self.api.transaction_commit(ptr, milliseconds))
        return count

    @RaiserTx.raise_if_error
    def rollback(self, timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Rolls back changes and finishes the transaction

        #### Arguments:
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum is 1 millisecond; if set to a lower value, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg = self._finish_native(
            lambda ptr: self.api.transaction_rollback(ptr, milliseconds))

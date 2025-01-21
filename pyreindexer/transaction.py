from datetime import timedelta
from typing import Dict, List

from pyreindexer.exceptions import ApiError, TransactionError


def raise_if_error(func):
    def wrapper(self, *args, **kwargs):
        self._raise_on_is_over()
        res = func(self, *args, **kwargs)
        self._raise_on_error()
        return res

    return wrapper


class Transaction:
    """An object representing the context of a Reindexer transaction

    #### Attributes:
        api (module): An API module for Reindexer calls
        transaction_wrapper_ptr (int): A memory pointer to Reindexer transaction object
        err_code (int): The API error code
        err_msg (string): The API error message

    """

    def __init__(self, api, transaction_wrapper_ptr: int):
        """Constructs a new Reindexer transaction object

        #### Arguments:
            api (module): An API module for Reindexer calls
            transaction_wrapper_ptr (int): A memory pointer to Reindexer transaction object

        """

        self.api = api
        self.transaction_wrapper_ptr: int = transaction_wrapper_ptr
        self.err_code: int = 0
        self.err_msg: str = ""

    def __del__(self):
        """Rollbacks a transaction if it was not previously stopped

        """

        if self.transaction_wrapper_ptr > 0:
            _, _ = self.api.rollback_transaction(self.transaction_wrapper_ptr)

    def _raise_on_error(self):
        """Checks if there is an error code and raises with an error message

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        if self.err_code:
            raise ApiError(self.err_msg)

    def _raise_on_is_over(self):
        """Checks the state of a transaction and returns an error message when necessary

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over

        """

        if self.transaction_wrapper_ptr <= 0:
            raise TransactionError("Transaction is over")

    @raise_if_error
    def insert(self, item_def: Dict, precepts: List[str] = None) -> None:
        """Inserts an item with its precepts to the transaction
            Warning: the timeout set when the transaction was created is used

        #### Arguments:
            item_def (dict): A dictionary of item definition
            precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        precepts = [] if precepts is None else precepts
        self.err_code, self.err_msg = self.api.item_insert_transaction(self.transaction_wrapper_ptr, item_def, precepts)

    @raise_if_error
    def update(self, item_def: Dict, precepts: List[str] = None) -> None:
        """Updates an item with its precepts to the transaction
            Warning: the timeout set when the transaction was created is used

        #### Arguments:
            item_def (dict): A dictionary of item definition
            precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        precepts = [] if precepts is None else precepts
        self.err_code, self.err_msg = self.api.item_update_transaction(self.transaction_wrapper_ptr, item_def, precepts)

    @raise_if_error
    def upsert(self, item_def: Dict, precepts: List[str] = None) -> None:
        """Updates an item with its precepts to the transaction. Creates the item if it not exists
            Warning: the timeout set when the transaction was created is used

        #### Arguments:
            item_def (dict): A dictionary of item definition
            precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        precepts = [] if precepts is None else precepts
        self.err_code, self.err_msg = self.api.item_upsert_transaction(self.transaction_wrapper_ptr, item_def, precepts)

    @raise_if_error
    def delete(self, item_def: Dict) -> None:
        """Deletes an item from the transaction
            Warning: the timeout set when the transaction was created is used

        #### Arguments:
            item_def (dict): A dictionary of item definition

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.item_delete_transaction(self.transaction_wrapper_ptr, item_def)

    @raise_if_error
    def commit(self, timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Applies changes

        #### Arguments:
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg, _ = self.api.commit_transaction(self.transaction_wrapper_ptr, milliseconds)
        self.transaction_wrapper_ptr = 0

    @raise_if_error
    def commit_with_count(self, timeout: timedelta = timedelta(milliseconds=0)) -> int:
        """Applies changes and return the number of count of changed items

        #### Arguments:
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg, count = self.api.commit_transaction(self.transaction_wrapper_ptr, milliseconds)
        self.transaction_wrapper_ptr = 0
        return count

    @raise_if_error
    def rollback(self, timeout: timedelta = timedelta(milliseconds=0)) -> None:
        """Rollbacks changes

        #### Arguments:
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Raises:
            TransactionError: Raises with an error message of API return if Transaction is over
            ApiError: Raises with an error message of API return on non-zero error code

        """

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg = self.api.rollback_transaction(self.transaction_wrapper_ptr, milliseconds)
        self.transaction_wrapper_ptr = 0

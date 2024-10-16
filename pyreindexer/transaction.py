class Transaction:
    """ An object representing the context of a Reindexer transaction

    # Attributes:
        api (module): An API module for Reindexer calls
        transaction_wrapper_ptr (int): A memory pointer to Reindexer transaction object
        err_code (int): the API error code
        err_msg (string): the API error message

    """

    def __init__(self, api, transaction_wrapper_ptr):
        """Constructs a new Reindexer transaction object

        # Arguments:
            api (module): An API module for Reindexer calls
            transaction_wrapper_ptr (int): A memory pointer to Reindexer transaction object

        """

        self.api = api
        self.transaction_wrapper_ptr = transaction_wrapper_ptr
        self.err_code = 0
        self.err_msg = ""

    def __del__(self):
        """Roll back a transaction if it was not previously stopped

        """

        if self.transaction_wrapper_ptr > 0:
            _, _ = self.api.rollback_transaction(self.transaction_wrapper_ptr)

    def _raise_on_error(self):
        """Checks if there is an error code and raises with an error message

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        if self.err_code:
            raise Exception(self.err_msg)

    def _raise_on_is_over(self):
        """Checks if there is an error code and raises with an error message

        # Raises:
            Exception: Raises with an error message of API return if Transaction is over

        """

        if self.transaction_wrapper_ptr <= 0:
            raise Exception("Transaction is over")

    def insert(self, item_def, precepts=None):
        """Inserts an item with its precepts to the transaction

        # Arguments:
            item_def (dict): A dictionary of item definition
            precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

        # Raises:
            Exception: Raises with an error message of API return if Transaction is over
            Exception: Raises with an error message of API return on non-zero error code

        """

        self._raise_on_is_over()
        if precepts is None:
            precepts = []
        self.err_code, self.err_msg = self.api.item_insert_transaction(self.transaction_wrapper_ptr, item_def, precepts)
        self._raise_on_error()

    def update(self, item_def, precepts=None):
        """Update an item with its precepts to the transaction

        # Arguments:
            item_def (dict): A dictionary of item definition
            precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

        # Raises:
            Exception: Raises with an error message of API return if Transaction is over
            Exception: Raises with an error message of API return on non-zero error code

        """

        self._raise_on_is_over()
        if precepts is None:
            precepts = []
        self.err_code, self.err_msg = self.api.item_update_transaction(self.transaction_wrapper_ptr, item_def, precepts)
        self._raise_on_error()

    def upsert(self, item_def, precepts=None):
        """Update an item with its precepts to the transaction. Creates the item if it not exists

        # Arguments:
            item_def (dict): A dictionary of item definition
            precepts (:obj:`list` of :obj:`str`): A dictionary of index definition

        # Raises:
            Exception: Raises with an error message of API return if Transaction is over
            Exception: Raises with an error message of API return on non-zero error code

        """

        self._raise_on_is_over()
        if precepts is None:
            precepts = []
        self.err_code, self.err_msg = self.api.item_upsert_transaction(self.transaction_wrapper_ptr, item_def, precepts)
        self._raise_on_error()

    def delete(self, item_def):
        """Delete an item from the transaction

        # Arguments:
            item_def (dict): A dictionary of item definition

        # Raises:
            Exception: Raises with an error message of API return if Transaction is over
            Exception: Raises with an error message of API return on non-zero error code

        """

        self._raise_on_is_over()
        self.err_code, self.err_msg = self.api.item_delete_transaction(self.transaction_wrapper_ptr, item_def)
        self._raise_on_error()

    def commit(self):
        """Commit a transaction

        # Raises:
            Exception: Raises with an error message of API return if Transaction is over
            Exception: Raises with an error message of API return on non-zero error code

        """

        self._raise_on_is_over()
        self.err_code, self.err_msg = self.api.commit_transaction(self.transaction_wrapper_ptr)
        self.transaction_wrapper_ptr = 0
        self._raise_on_error()

    def rollback(self):
        """Roll back a transaction

        # Raises:
            Exception: Raises with an error message of API return if Transaction is over
            Exception: Raises with an error message of API return on non-zero error code

        """

        self._raise_on_is_over()
        self.err_code, self.err_msg = self.api.rollback_transaction(self.transaction_wrapper_ptr)
        self.transaction_wrapper_ptr = 0
        self._raise_on_error()

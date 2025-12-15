from pyreindexer.exceptions import ApiError, TransactionError


class RaiserRx:
    """Contains methods for checking some typical API bad events and raise if there is a necessity

    """
    err_code: int
    err_msg: str
    rx: int

    @staticmethod
    def raise_if_error(func):
        def wrapper(self, *args, **kwargs):
            self.raise_on_not_init()
            res = func(self, *args, **kwargs)
            self.raise_on_error()
            return res

        return wrapper

    def raise_on_error(self):
        """Checks if there is an error code and raises with an error message

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        if self.err_code:
            raise ApiError(self.err_msg)

    def raise_on_not_init(self):
        """Checks if there is an error code and raises with an error message

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet

        """

        if self.rx <= 0:
            raise ConnectionError("Connection is not initialized: reindexer C-binding object does not exist")


class RaiserQuery(RaiserRx):
    """Contains methods for checking some typical API bad events and raise if there is a necessity

    """
    rx: None

    def raise_on_not_init(self):
        """Checks if there is an error code and raises with an error message

        #### Raises:
            ConnectionError: Raises with an error message when Reindexer instance is not initialized yet

        """

        if self.rx.rx <= 0:
            raise ConnectionError("Connection is not initialized: reindexer C-binding object does not exist")


class RaiserTx(RaiserQuery):
    """Contains methods for checking some typical API bad events and raise if there is a necessity

    """
    transaction_wrapper_ptr: int

    @staticmethod
    def raise_if_error(func):
        def wrapper(self, *args, **kwargs):
            self.raise_on_not_init()
            self.raise_on_is_over()
            res = func(self, *args, **kwargs)
            self.raise_on_error()
            return res

        return wrapper

    def raise_on_is_over(self):
        """Checks if there is an error code and raises with an error message

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        if self.transaction_wrapper_ptr <= 0:
            raise TransactionError("Transaction is over")

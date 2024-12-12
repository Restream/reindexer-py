from pyreindexer.exceptions import ApiError


class RaiserMixin:
    """RaiserMixin contains methods for checking some typical API bad events and raise if there is a necessity

    """
    err_code: int
    err_msg: str
    rx: int

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
            raise ConnectionError("Connection is not initialized")


def raise_if_error(func):
    def wrapper(self, *args, **kwargs):
        self.raise_on_not_init()
        res = func(self, *args, **kwargs)
        self.raise_on_error()
        return res

    return wrapper

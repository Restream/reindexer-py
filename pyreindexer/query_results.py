from pyreindexer.exceptions import ApiError


class QueryResults:
    """QueryResults is a disposable iterator of Reindexer results for such queries as SELECT etc.
        When the results are fetched the iterator closes and frees a memory of results buffer of Reindexer

    #### Attributes:
        api (module): An API module for Reindexer calls
        err_code (int): The API error code
        err_msg (string): The API error message
        qres_wrapper_ptr (int): A memory pointer to Reindexer iterator object
        qres_iter_count (int): A count of results for iterations
        pos (int): The current result position in iterator

    """

    def __init__(self, api, qres_wrapper_ptr, qres_iter_count, qres_total_count):
        """Constructs a new Reindexer query results iterator object

        #### Arguments:
            api (module): An API module for Reindexer calls
            qres_wrapper_ptr (int): A memory pointer to Reindexer iterator object
            qres_iter_count (int): A count of results for iterations
            qres_total_count (int): A total or cached count of results

        """

        self.api = api
        self.qres_wrapper_ptr = qres_wrapper_ptr
        self.qres_iter_count = qres_iter_count
        self.qres_total_count = qres_total_count
        self.pos = 0
        self.err_code = 0
        self.err_msg = ""

    def __raise_on_error(self):
        """Checks if there is an error code and raises with an error message

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        if self.err_code:
            raise ApiError(self.err_msg)

    def __iter__(self):
        """Returns the current iteration result

        """

        return self

    def __next__(self):
        """Returns the next iteration result

        #### Raises:
            StopIteration: Frees results on end of iterator and raises with iteration stop

        """

        if self.pos < self.qres_iter_count:
            self.pos += 1
            self.err_code, self.err_msg, res = self.api.query_results_iterate(self.qres_wrapper_ptr)
            self.__raise_on_error()
            return res
        else:
            del self
            raise StopIteration

    def __del__(self):
        """Calls close iterator method on an iterator object deletion

        """

        self._close_iterator()

    def status(self) -> None:
        """Check status

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.query_results_status(self.qres_wrapper_ptr)
        self.__raise_on_error()

    def count(self) -> int:
        """Returns a count of results for iterations

        #### Returns
            int: A count of results

        """

        return self.qres_iter_count

    def total_count(self) -> int:
        """Returns a total or cached count of results

        #### Returns
            int: A total or cached count of results

        """

        return self.qres_total_count

    def _close_iterator(self) -> None:
        """Frees query results for the current iterator

        """

        self.qres_iter_count = 0
        self.api.query_results_delete(self.qres_wrapper_ptr)

    def get_agg_results(self) -> dict:
        """Returns aggregation results for the current query

        #### Returns
            (:obj:`dict`): Dictionary with all results for the current query

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg, res = self.api.get_agg_results(self.qres_wrapper_ptr)
        self.__raise_on_error()
        return res

    def get_explain_results(self) -> str:
        """Returns explain results for the current query

        #### Returns
            (string): Formatted string with explain of results for the current query

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg, res = self.api.get_explain_results(self.qres_wrapper_ptr)
        self.__raise_on_error()
        return res

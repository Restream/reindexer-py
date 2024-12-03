class ApiError(Exception):
    pass


class QueryError(ApiError):
    pass


class QueryResultsError(QueryError):
    pass


class TransactionError(ApiError):
    pass

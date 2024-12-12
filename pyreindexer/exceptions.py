class ApiError(Exception):
    pass


class QueryError(ApiError):
    pass


class TransactionError(ApiError):
    pass

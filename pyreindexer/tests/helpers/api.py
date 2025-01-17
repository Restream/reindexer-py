from datetime import timedelta

from pyreindexer import RxConnector
from query import Query
from tests.helpers.log_helper import log_api


def make_request_and_response_log(method_description, call_msg, res=None) -> str:
    return f"{method_description}\n\t[Call] => {call_msg}\n\t[Return] <= {res}"


def api_method(func):
    def wrapped(self, *args, **kwargs):
        try:
            method_description = func.__doc__.split("\n")[0]
        except AttributeError:
            raise RuntimeError("Api Method doesn't have a 'docstring' description")

        args_str = ", ".join(repr(a) for a in args)
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        call_msg = f"args ({args_str}), kwargs ({kwargs_str})"

        r = func(self, *args, **kwargs)
        log = make_request_and_response_log(method_description, call_msg, r)
        log_api.info(log)
        return r

    return wrapped


class ConnectorApi(RxConnector):

    def __init__(self, dsn, **kwargs):
        super().__init__(dsn, **kwargs)
        self.namespace = NamespaceApiMethods(self)
        self.index = IndexApiMethods(self)
        self.item = ItemApiMethods(self)
        self.query = QueryApiMethods(self)
        self.meta = MetaApiMethods(self)
        self.tx = TransactionApiMethods(self)

    default_timeout: timedelta = timedelta(milliseconds=0)


class NamespaceApiMethods:
    def __init__(self, api):
        self.api = api

    @api_method
    def open(self, ns_name, timeout: timedelta = ConnectorApi.default_timeout):
        """ Open namespace """
        return self.api.namespace_open(ns_name, timeout)

    @api_method
    def close(self, ns_name, timeout: timedelta = ConnectorApi.default_timeout):
        """ Close namespace """
        return self.api.namespace_close(ns_name, timeout)

    @api_method
    def drop(self, ns_name, timeout: timedelta = ConnectorApi.default_timeout):
        """ Drop namespace """
        return self.api.namespace_drop(ns_name, timeout)

    @api_method
    def enumerate(self, enum_not_opened=False, timeout: timedelta = ConnectorApi.default_timeout):
        """ Get namespaces list """
        return self.api.namespaces_enum(enum_not_opened, timeout)


class IndexApiMethods:
    def __init__(self, api):
        self.api = api

    @api_method
    def create(self, ns_name, index, timeout: timedelta = ConnectorApi.default_timeout):
        """ Add index """
        return self.api.index_add(ns_name, index, timeout)

    @api_method
    def update(self, ns_name, index, timeout: timedelta = ConnectorApi.default_timeout):
        """ Update index """
        return self.api.index_update(ns_name, index, timeout)

    @api_method
    def drop(self, ns_name, index_name, timeout: timedelta = ConnectorApi.default_timeout):
        """ Drop index """
        return self.api.index_drop(ns_name, index_name, timeout)


class ItemApiMethods:
    def __init__(self, api):
        self.api = api

    @api_method
    def insert(self, ns_name, item, precepts=None, timeout: timedelta = ConnectorApi.default_timeout):
        """ Insert item """
        return self.api.item_insert(ns_name, item, precepts, timeout)

    @api_method
    def upsert(self, ns_name, item, precepts=None, timeout: timedelta = ConnectorApi.default_timeout):
        """ Upsert item """
        return self.api.item_upsert(ns_name, item, precepts, timeout)

    @api_method
    def update(self, ns_name, item, precepts=None, timeout: timedelta = ConnectorApi.default_timeout):
        """ Update item """
        return self.api.item_update(ns_name, item, precepts, timeout)

    @api_method
    def delete(self, ns_name, item, timeout: timedelta = ConnectorApi.default_timeout):
        """ Delete item """
        return self.api.item_delete(ns_name, item, timeout)


class QueryApiMethods:
    def __init__(self, api):
        self.api = api

    @api_method
    def sql(self, q, timeout: timedelta = ConnectorApi.default_timeout):
        """ Execute SQL query """
        return self.api.select(q, timeout)

    @api_method
    def new(self, ns_name) -> Query:
        """ Create a new query """
        return self.api.new_query(ns_name)


class MetaApiMethods:
    def __init__(self, api):
        self.api = api

    @api_method
    def put(self, ns_name, key, value, timeout: timedelta = ConnectorApi.default_timeout):
        """ Put meta with key and value """
        return self.api.meta_put(ns_name, key, value, timeout)

    @api_method
    def get(self, ns_name, key, timeout: timedelta = ConnectorApi.default_timeout):
        """ Get meta by key """
        return self.api.meta_get(ns_name, key, timeout)

    @api_method
    def enumerate(self, ns_name, timeout: timedelta = ConnectorApi.default_timeout):
        """ Get meta keys list """
        return self.api.meta_enum(ns_name, timeout)

    @api_method
    def delete(self, ns_name, key, timeout: timedelta = ConnectorApi.default_timeout):
        """ Delete meta by key """
        return self.api.meta_delete(ns_name, key, timeout)


class TransactionApiMethods:
    def __init__(self, api):
        self.api = api

    class _TransactionApi:
        def __init__(self, tx):
            self.tx = tx

        @api_method
        def commit(self, timeout: timedelta = ConnectorApi.default_timeout):
            """ Commit the transaction """
            return self.tx.commit(timeout)

        @api_method
        def commit_with_count(self, timeout: timedelta = ConnectorApi.default_timeout):
            """ Commit the transaction and return the number of changed items """
            return self.tx.commit_with_count(timeout)

        @api_method
        def rollback(self, timeout: timedelta = ConnectorApi.default_timeout):
            """ Rollback the transaction """
            return self.tx.rollback(timeout)

        @api_method
        def insert_item(self, item, precepts=None):
            """ Insert item into transaction """
            return self.tx.insert(item, precepts)

        @api_method
        def upsert_item(self, item, precepts=None):
            """ Upsert item into transaction """
            return self.tx.upsert(item, precepts)

        @api_method
        def update_item(self, item, precepts=None):
            """ Update item into transaction """
            return self.tx.update(item, precepts)

        @api_method
        def delete_item(self, item):
            """ Delete item from transaction """
            return self.tx.delete(item)

        @api_method
        def update_query(self, query):
            """ Call update query in transaction """
            return self.tx.update_query(query)

        @api_method
        def delete_query(self, query):
            """ Call delete query in transaction """
            return self.tx.delete_query(query)

    @api_method
    def begin(self, ns_name, timeout: timedelta = ConnectorApi.default_timeout) -> "_TransactionApi":
        """ Begin new transaction """
        tx = self.api.new_transaction(ns_name, timeout)
        return self._TransactionApi(tx)

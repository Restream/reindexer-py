from pyreindexer import RxConnector
from tests.helpers.log_helper import log_api


def make_request_and_response_log(method_description, request_msg, res=None) -> str:
    return f"{method_description}\n\t[Request] => {request_msg}\n\t[Response] => {res}"


def api_method(func):
    def wrapped(self, *args, **kwargs):
        try:
            method_description = func.__doc__.split("\n")[0]
        except AttributeError:
            raise RuntimeError("Api Method doesn't have a 'docstring' description")

        args_str = ", ".join(repr(a) for a in args)
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        request_msg = f"Called {func.__name__} with args ({args_str}) and kwargs ({kwargs_str})"

        r = func(self, *args, **kwargs)
        log = make_request_and_response_log(method_description, request_msg, r)
        log_api.info(log)
        return r

    return wrapped


class ConnectorApi(RxConnector):

    def __init__(self, dsn):
        super().__init__(dsn)
        self.namespace = NamespaceApiMethods(self)
        self.index = IndexesApiMethods(self)
        self.item = ItemApiMethods(self)
        self.query = QueryApiMethods(self)
        self.meta = MetaApiMethods(self)


class NamespaceApiMethods:
    def __init__(self, api):
        self.api = api

    @api_method
    def open(self, ns_name):
        """ Open namespace """
        return self.api.namespace_open(ns_name)

    @api_method
    def close(self, ns_name):
        """ Close namespace """
        return self.api.namespace_close(ns_name)

    @api_method
    def drop(self, ns_name):
        """ Drop namespace """
        return self.api.namespace_drop(ns_name)

    @api_method
    def enumerate(self, enum_not_opened=False):
        """ Get namespaces list """
        return self.api.namespaces_enum(enum_not_opened)


class IndexesApiMethods:
    def __init__(self, api):
        self.api = api

    @api_method
    def create(self, ns_name, index):
        """ Add index """
        return self.api.index_add(ns_name, index)

    @api_method
    def update(self, ns_name, index):
        """ Update index """
        return self.api.index_update(ns_name, index)

    @api_method
    def drop(self, ns_name, index_name):
        """ Drop index """
        return self.api.index_drop(ns_name, index_name)


class ItemApiMethods:
    def __init__(self, api):
        self.api = api

    @api_method
    def insert(self, ns_name, item, precepts=None):
        """ Insert item """
        return self.api.item_insert(ns_name, item, precepts)

    @api_method
    def upsert(self, ns_name, item, precepts=None):
        """ Upsert item """
        return self.api.item_upsert(ns_name, item, precepts)

    @api_method
    def update(self, ns_name, item, precepts=None):
        """ Update item """
        return self.api.item_update(ns_name, item, precepts)

    @api_method
    def delete(self, ns_name, item):
        """ Delete item """
        return self.api.item_delete(ns_name, item)


class QueryApiMethods:
    def __init__(self, api):
        self.api = api

    @api_method
    def sql(self, q):
        """ Execute SQL query """
        return self.api.select(q)


class MetaApiMethods:
    def __init__(self, api):
        self.api = api

    @api_method
    def put(self, ns_name, key, value):
        """ Put meta with key and value """
        return self.api.meta_put(ns_name, key, value)

    @api_method
    def get(self, ns_name, key):
        """ Get meta by key """
        return self.api.meta_get(ns_name, key)

    @api_method
    def enumerate(self, ns_name):
        """ Get meta keys list """
        return self.api.meta_enum(ns_name)

    @api_method
    def delete(self, ns_name, key):
        """ Delete meta by key """
        return self.api.meta_delete(ns_name, key)

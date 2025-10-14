import os
import platform
import shutil
from datetime import timedelta
from pathlib import Path

import pytest
from hamcrest import *

from pyreindexer.exceptions import ApiError
from pyreindexer.query import CondType
from tests.helpers.api import ConnectorApi
from tests.helpers.base_helper import get_ns_description, get_ns_items
from tests.helpers.server_helper import ReindexerServer
from tests.test_data.auth import users_yml
from tests.test_data.constants import index_definition, item_definition


CONNECTIONS = []


@pytest.fixture(scope="module", autouse=True)
def rx_server(request):
    if request.config.getoption("--mode") == "builtin":
        pytest.skip("auth tests run only for cproto mode")
    else:
        rx_bin_path = request.config.getoption("--rx_bin_path")
        storage = f"/tmp/reindex_test_auth"
        if os.path.exists(storage):
            shutil.rmtree(storage, ignore_errors=True)
        Path(storage).mkdir(parents=True)
        with open(os.path.join(storage, "users.yml"), "w") as file:
            file.write(users_yml)

        server = ReindexerServer(rx_bin_path=rx_bin_path, http_port=9089, rpc_port=6535, storage=storage, auth=True,
                                 user="owner", password="owner")
        server.run(module=request.node.nodeid)
        yield
        server.terminate()


@pytest.fixture(scope="module")
def db(request):
    db = ConnectorApi("cproto://owner:owner@127.0.0.1:6535/test_db")
    yield db
    db.close()
    shutil.rmtree("tmp/", ignore_errors=True)


@pytest.fixture
def db_auth(request):
    def _inner(auth):
        db = ConnectorApi(f"cproto://{auth[0]}:{auth[1]}@127.0.0.1:6535/test_db")
        CONNECTIONS.append(db)
        return db

    yield _inner


@pytest.fixture(autouse=True)
def close_connections(db, db_auth):
    yield
    for db_conn in CONNECTIONS:
        db_conn.close()
    for ns in db.namespace.enumerate():
        if not ns["name"].startswith("#"):
            db.namespace.drop(ns["name"])
    CONNECTIONS.clear()


class TestAuth:

    @pytest.mark.skipif(platform.system().lower() == "darwin", reason="doesn't work on Mac OS for now")
    def test_cant_connect_to_db_with_invalid_pass(self, db_auth):
        # When ("Connect to DB")
        # Then ("Connection is not established")
        auth = ("invalid_pass", "invalid_pass")
        err_msg = f"Errors occurred when parsing the URL to mask user credentials"
        assert_that(calling(db_auth).with_args(auth),
                    raises(ApiError, pattern=err_msg))

    @pytest.mark.parametrize("auth", [
        ("owner", "owner"),
        ("db_admin", "dbadmin"),
        ("data_write", "datawrite"),
        ("data_read", "dataread")
    ])
    def test_auth_db_admin_can_open_namespace(self, db_auth, auth):
        # When ("Open namespace")
        # Then ("Namespace is opened")
        ns_name = "new_ns_auth"
        db_auth = db_auth(auth)
        db_auth.namespace.open(ns_name)

    @pytest.mark.parametrize("auth, err_msg", [
        (("error", "error"), "Unauthorized")
    ])
    def test_unauthorized_user_cant_open_namespace(self, db_auth, auth, err_msg):
        # When ("Open namespace")
        # Then ("Namespace is not opened")
        ns_name = "new_ns_auth"
        db_auth = db_auth(auth)
        assert_that(calling(db_auth.namespace.open).with_args(ns_name),
                    raises(ApiError, pattern=err_msg))

    @pytest.mark.parametrize("auth", [
        ("owner", "owner"),
        ("db_admin", "dbadmin"),
        ("data_write", "datawrite"),
        ("data_read", "dataread")
    ])
    def test_all_auth_users_can_get_namespaces_list(self, db, namespace, db_auth, auth):
        # When ("Get namespaces list")
        ns_name = "new_ns_auth"
        db_auth = db_auth(auth)
        namespaces_list = db_auth.namespace.enumerate()
        # Then ("Namespaces list is returned")
        assert_that(namespaces_list, has_item(has_entries(name=namespace)))

    @pytest.mark.parametrize("auth", [
        ("owner", "owner"),
        ("db_admin", "dbadmin"),
        ("data_write", "datawrite"),
        ("data_read", "dataread")
    ])
    def test_all_auth_users_can_sql_select(self, db, db_auth, namespace, index, item, auth):
        # Given("Create namespace with id and item")
        # When ("Execute SQL query SELECT")
        db_auth = db_auth(auth)
        query = f"SELECT * FROM {namespace}"
        items_list = list(db_auth.query.sql(query))
        # Then ("Check that selected item is in result")
        assert_that(items_list, equal_to([item]))

    @pytest.mark.parametrize("auth", [
        ("data_write", "datawrite"),
        ("data_read", "dataread")
    ])
    def test_auth_data_write_cant_create_index(self, db, db_auth, namespace, auth):
        # Given("Create namespace")
        # When ("Create index")
        # Then ("Index is not created")
        db_auth = db_auth(auth)
        role = auth[0]
        err_msg = f"Forbidden: need role db_admin of db 'test_db' user 'da...{role[-2:]}' have role={role}"
        assert_that(calling(db_auth.index.create).with_args(namespace, index_definition),
                    raises(ApiError, pattern=err_msg))

    @pytest.mark.parametrize("auth", [
        ("owner", "owner"),
        ("db_admin", "dbadmin")
    ])
    def test_auth_db_admin_can_create_index(self, db, db_auth, namespace, auth):
        # Given("Create namespace")
        # When ("Create index")
        db_auth = db_auth(auth)
        db_auth.index.create(namespace, index_definition)
        # Then ("Index is created")
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(index_definition))))

    @pytest.mark.parametrize("auth", [
        ("owner", "owner"),
        ("db_admin", "dbadmin"),
        ("data_write", "datawrite"),
        ("data_read", "dataread")
    ])
    def test_all_auth_users_can_query_select_where(self, db, db_auth, namespace, index, items, auth):
        # Given("Create namespace with index and items")
        # When ("Make select query")
        db_auth = db_auth(auth)
        query = db_auth.query.new(namespace)
        query_result = list(query.where("id", CondType.CondEq, 3).execute(timeout=timedelta(seconds=1)))
        # Then ("Check that selected item is in result")
        assert_that(query_result, equal_to([items[3]]))

    @pytest.mark.parametrize("auth", [
        ("owner", "owner"),
        ("db_admin", "dbadmin"),
        ("data_write", "datawrite")
    ])
    def test_auth_data_write_can_tx_item_insert(self, db, db_auth, namespace, index, auth):
        # Given("Create namespace with index")
        # When ("Insert item into namespace via tx")
        db_auth = db_auth(auth)
        transaction = db_auth.tx.begin(namespace)
        transaction.insert_item(item_definition)
        transaction.commit(timeout=timedelta(milliseconds=1000))
        # Then ("Item was added")
        select_result = get_ns_items(db_auth, namespace)
        assert_that(select_result, equal_to([item_definition]))

    def test_auth_data_read_cant_begin_tx(self, db, db_auth, namespace, index):
        # Given("Create namespace with index")
        # When ("Begin transaction")
        # then ("Transaction is not started")
        db_auth = db_auth(("data_read", "dataread"))
        err_msg = "Forbidden: need role data_write of db 'test_db' user 'da...ad' have role=data_read"
        assert_that(calling(db_auth.tx.begin).with_args(namespace), raises(ApiError, pattern=err_msg))

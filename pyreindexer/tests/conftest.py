import shutil

import pytest

from pyreindexer.tests.helpers.api import ConnectorApi
from pyreindexer.tests.helpers.log_helper import log_fixture
from pyreindexer.tests.test_data.constants import index_definition, item_definition


def pytest_addoption(parser):
    parser.addoption("--mode", choices=["builtin", "cproto"], default="builtin", help="Connection mode")


@pytest.fixture(scope="session", autouse=True)
def log_setup(request):
    log_fixture.info("Work with pyreindexer connector using {} mode".format(request.config.getoption("--mode")))


@pytest.fixture(scope="session")
def db(request):
    """
    Create a database
    """
    mode = request.config.getoption('--mode')
    db_name = 'test_db'
    prefix = "builtin://tmp/" if mode == "builtin" else "cproto://127.0.0.1:6534/"
    db = ConnectorApi(f"{prefix}{db_name}")
    yield db
    db.close()
    shutil.rmtree('tmp/', ignore_errors=True)


@pytest.fixture(scope="function")
def namespace(db):
    """
    Create a namespace
    """
    ns_name = 'new_ns'
    db.namespace.open(ns_name)
    yield ns_name
    db.namespace.drop(ns_name)


@pytest.fixture(scope="function")
def index(db, namespace):
    """
    Create an index to namespace
    """
    db.index.create(namespace, index_definition)
    yield
    db.index.drop(namespace, "id")


@pytest.fixture(scope="function")
def item(db, namespace):
    """
    Create an item to namespace
    """
    db.item.insert(namespace, item_definition)
    yield item_definition
    db.item.delete(namespace, item_definition)


@pytest.fixture(scope="function")
def items(db, namespace):
    """
    Create items to namespace
    """
    items = [{"id": i, "val": f"testval{i}"} for i in range(10)]
    for item in items:
        db.item.insert(namespace, item)
    yield items
    for item in items:
        db.item.delete(namespace, item)


@pytest.fixture(scope="function")
def metadata(db, namespace):
    """
    Put metadata  to namespace
    """
    key, value = 'key', 'value'
    db.meta.put(namespace, key, value)
    yield key, value


@pytest.fixture(scope="function")
def second_namespace_for_join(db):
    second_namespace_name = 'test_ns_for_join'
    db.namespace.open(second_namespace_name)
    db.index.create(second_namespace_name, index_definition)
    second_ns_item_definition = {"id": 100, "second_ns_val": "second_ns_testval"}
    second_ns_item_definition_join = {"id": 1, "second_ns_val": "second_ns_testval_1"}
    db.item.insert(second_namespace_name, second_ns_item_definition)
    db.item.insert(second_namespace_name, second_ns_item_definition_join)
    yield second_namespace_name, second_ns_item_definition_join

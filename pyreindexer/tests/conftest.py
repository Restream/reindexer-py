import shutil
import pytest

from pyreindexer import RxConnector
from tests.helpers.index import *
from tests.helpers.items import *
from tests.helpers.log_helper import log_fixture
from tests.helpers.metadata import put_metadata
from tests.helpers.namespace import *
from tests.test_data.constants import index_definition, item_definition


def pytest_addoption(parser):
    parser.addoption("--mode", action="store", default='builtin', help='builtin or cproto')


@pytest.fixture(scope="session", autouse=True)
def log_setup(request):
    """ Execute once before test run
    """
    log_fixture.info("Work with pyreindexer connector using {} mode".format(request.config.getoption("--mode")))


@pytest.fixture(scope="session")
def database(request):
    """
    Create a database
    """
    mode = request.config.getoption('--mode')
    db_name = 'test_db'
    if mode == 'builtin':
        prefix = 'builtin://tmp/'
    elif mode == 'cproto':
        prefix = 'cproto://127.0.0.1:6534/'
    else:
        raise ConnectionError
    db = RxConnector(prefix + db_name)
    yield db, db_name
    db.close()
    shutil.rmtree('tmp/', ignore_errors=True)


@pytest.fixture(scope="function")
def namespace(database):
    """
    Create a namespace
    """
    db, db_name = database
    ns_name = 'new_ns'
    create_namespace(database, ns_name)
    yield db, ns_name
    drop_namespace(database, ns_name)


@pytest.fixture(scope="function")
def index(namespace):
    """
    Create an index to namespace
    """
    create_index(namespace, index_definition)
    yield
    drop_index(namespace, 'id')


@pytest.fixture(scope="function")
def item(namespace):
    """
    Create an item to namespace
    """
    insert_item(namespace, item_definition)
    yield item_definition
    delete_item(namespace, item_definition)


@pytest.fixture(scope="function")
def items(namespace):
    """
    Create items to namespace
    """
    for i in range(10):
        insert_item(namespace, {"id": i+1, "val": "testval" + str(i+1)})
    yield
    for i in range(10):
        delete_item(namespace, {"id": i+1, "val": "testval" + str(i+1)})


@pytest.fixture(scope="function")
def metadata(namespace):
    """
    Put metadata  to namespace
    """
    key, value = 'key', 'value'
    put_metadata(namespace, key, value)
    yield key, value


@pytest.fixture(scope="function")
def second_namespace_for_join(database):
    db, db_name = database
    second_namespace_name = 'test_ns_for_join'
    db.namespace_open(second_namespace_name)
    db.index_add(second_namespace_name, index_definition)
    second_ns_item_definition = {"id": 100, "second_ns_val": "second_ns_testval"}
    second_ns_item_definition_join = {"id": 1, "second_ns_val": "second_ns_testval_1"}
    db.item_insert(second_namespace_name, second_ns_item_definition)
    db.item_insert(second_namespace_name, second_ns_item_definition_join)
    yield second_namespace_name, second_ns_item_definition_join

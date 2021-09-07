import shutil
import pytest

from pyreindexer import RxConnector
from qa_test.helpers.index import *
from qa_test.helpers.items import *
from qa_test.helpers.log_helper import log_fixture
from qa_test.helpers.namespace import *
from qa_test.test_data.constants import index_definition, item_definition


def pytest_addoption(parser):
    parser.addoption("--mode", action="store", default='builtin', help='builtin or cproto')


@pytest.fixture(scope="session", autouse=True)
def log_setup(request):
    """ Выполняется один раз, до запуска всех тестов и после окончания всех тестов
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


@pytest.fixture(scope="session")
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
def metadata(namespace):
    """
    Put metadata  to namespace
    """
    db, namespace_name = namespace
    key, value = 'key', 'value'
    db.meta_put(namespace_name, key, value)
    yield key, value


import random
import shutil

import pytest

from tests.helpers.api import ConnectorApi
from tests.helpers.log_helper import log_fixture
from tests.test_data.constants import composite_index_definition, index_definition, item_definition


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


@pytest.fixture
def namespace(db):
    """
    Create a namespace
    """
    ns_name = 'new_ns'
    db.namespace.open(ns_name)
    yield ns_name
    db.namespace.drop(ns_name)


@pytest.fixture
def index(db, namespace):
    """
    Create an index to namespace
    """
    db.index.create(namespace, index_definition)
    yield


@pytest.fixture
def sparse_index(db, namespace):
    """
    Create sparse index to namespace
    """
    db.index.create(namespace, {"name": "val", "json_paths": ["val"], "field_type": "string", "index_type": "hash",
                                "is_sparse": True})
    yield


@pytest.fixture
def indexes(db, namespace):
    """
    Create two indexes to namespace
    """
    db.index.create(namespace, index_definition)
    db.index.create(namespace, {"name": "val", "json_paths": ["val"], "field_type": "string", "index_type": "hash"})
    yield


@pytest.fixture
def item(db, namespace):
    """
    Create an item to namespace
    """
    db.item.insert(namespace, item_definition)
    yield item_definition


@pytest.fixture
def items(db, namespace):
    """
    Create items to namespace
    """
    items = [{"id": i, "val": f"testval{i}"} for i in range(10)]
    for item in items:
        db.item.insert(namespace, item)
    yield items


@pytest.fixture
def items_shuffled(db, namespace):
    """
    Create items in random order
    """
    items = [{"id": i, "val": f"testval{i}"} for i in range(5)]
    random.shuffle(items)
    for item in items:
        db.item.insert(namespace, item)
    yield items


@pytest.fixture
def composite_index(db, namespace):
    """
    Create indexes and composite index from them
    """
    db.index.create(namespace, index_definition)
    db.index.create(namespace, {"name": "val", "json_paths": ["val"], "field_type": "string", "index_type": "hash"})
    db.index.create(namespace, composite_index_definition)
    yield


@pytest.fixture
def rtree_index_and_items(db, namespace):
    """
    Create rtree index and items
    """
    db.index.create(namespace, {"name": "rtree", "json_paths": ["rtree"], "field_type": "point",
                                "index_type": "rtree", "rtree_type": "rstar"})
    items = [{"id": i, "rtree": [i, i]} for i in range(10)]
    for item in items:
        db.item.insert(namespace, item)
    yield items


@pytest.fixture
def ft_index_and_items(db, namespace):
    """
    Create rtree index and items
    """
    db.index.create(namespace, {"name": "ft", "json_paths": ["ft"], "field_type": "string", "index_type": "text"})
    content = ["one word", "sword two", "three work 333"]
    items = [{"id": i, "ft": c} for i, c in enumerate(content)]
    for item in items:
        db.item.insert(namespace, item)
    yield items


@pytest.fixture
def array_index_and_items(db, namespace):
    """
    Create rtree index and items
    """
    db.index.create(namespace, {"name": "arr", "json_paths": ["arr"], "field_type": "int", "index_type": "tree",
                                "is_array": True})
    items = [{"id": i, "arr": [i, i + 1]} for i in range(5)]
    for item in items:
        db.item.insert(namespace, item)
    yield items


@pytest.fixture
def index_and_duplicate_items(db, namespace):
    """
    Create index and items with duplicate value
    """
    db.index.create(namespace, {"name": "idx", "json_paths": ["idx"], "field_type": "int", "index_type": "hash"})
    items = [{"id": 0, "idx": 0}, {"id": 1, "idx": 1}, {"id": 2, "idx": 1}, {"id": 3, "idx": 3}]
    for item in items:
        db.item.insert(namespace, item)
    yield items


@pytest.fixture
def array_indexes_and_items(db, namespace):
    """
    Create array indexes and items
    """
    db.index.create(namespace, {"name": "arr1", "json_paths": ["arr1"], "field_type": "int",
                                "index_type": "tree", "is_array": True})
    db.index.create(namespace, {"name": "arr2", "json_paths": ["arr2"], "field_type": "int",
                                "index_type": "tree", "is_array": True})
    items = [{"id": i, "arr1": [i, i % 2], "arr2": [i % 2, i]} for i in range(5)]
    for item in items:
        db.item.insert(namespace, item)
    yield items


@pytest.fixture
def metadata(db, namespace):
    """
    Put metadata  to namespace
    """
    key, value = 'key', 'value'
    db.meta.put(namespace, key, value)
    yield key, value


@pytest.fixture
def second_namespace(db):
    second_namespace_name = "test_ns_for_join"
    db.namespace.open(second_namespace_name)
    db.index.create(second_namespace_name, index_definition)
    yield second_namespace_name
    db.namespace.drop(second_namespace_name)


@pytest.fixture
def second_item(db, second_namespace):
    """
    Create item for the second namespace
    """
    item = {"id": 1, "second_ns_val": "second_ns_testval_1"}
    db.item.insert(second_namespace, item)
    yield item


@pytest.fixture
def second_items(db, second_namespace):
    """
    Create more items for the second namespace
    """
    items = [{"id": i, "second_ns_val": f"second_ns_testval_{i}"} for i in range(1, 6)]
    for item in items:
        db.item.insert(second_namespace, item)
    yield items

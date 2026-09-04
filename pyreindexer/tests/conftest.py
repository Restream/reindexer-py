import random
import shutil

import pytest

from tests.helpers.api import ConnectorApi
from tests.helpers.base_helper import create_items, supplement_index
from tests.helpers.log_helper import log_fixture
from tests.helpers.server_helper import ReindexerServer
from tests.test_data.constants import composite_index_definition, index_definition, item_definition


def pytest_addoption(parser):
    parser.addoption("--mode", choices=["builtin", "cproto"], default="builtin", help="Connection mode")
    parser.addoption("--rx_bin_path", action="store", help="path to reindexer_server", default="")


@pytest.fixture(scope="session", autouse=True)
def log_setup(request):
    log_fixture.info("Work with pyreindexer connector using {} mode".format(request.config.getoption("--mode")))


@pytest.fixture(scope="module", autouse=True)
def rx_server(request):
    """
    Start reindexer server for cproto mode
    """
    if request.config.getoption("--mode") == "builtin":
        yield
    else:
        rx_bin_path = request.config.getoption("--rx_bin_path")
        module = request.node.nodeid.replace(":", "_")
        server = ReindexerServer(rx_bin_path=rx_bin_path, http_port=9088, rpc_port=6534,
                                 storage=f"/tmp/reindex_test_{module}")
        server.run(module=module)
        yield
        server.terminate()


@pytest.fixture(scope="module")
def db(request):
    """
    Create a database
    """
    mode = request.config.getoption("--mode")
    prefix = "builtin://tmp/" if mode == "builtin" else "cproto://127.0.0.1:6534/"
    db_name = "test_db"
    db = ConnectorApi(f"{prefix}{db_name}")
    yield db
    db.close()
    shutil.rmtree("tmp/", ignore_errors=True)


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
    create_items(db, namespace, items)
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


@pytest.fixture(scope="class")
def nested_join_nss(db):
    def create_ns(ns_name, indexes):
        db.namespace.open(ns_name)
        for idx in indexes:
            supplement_index(idx)
            db.index.create(ns_name, idx)
        return ns_name

    books = create_ns("books", [
        {"is_pk": True, "name": "id", "field_type": "int"},
        {"name": "author_id", "field_type": "int", "index_type": "tree"},
        {"name": "price", "field_type": "int", "index_type": "tree"},
    ])
    authors = create_ns("authors", [
        {"is_pk": True, "name": "id", "field_type": "int"},
        {"name": "j_id", "field_type": "int"},
        {"name": "location_id", "field_type": "int", "index_type": "tree"},
        {"name": "age", "field_type": "int", "index_type": "tree"},
    ])
    locations = create_ns("locations", [
        {"is_pk": True, "name": "id", "field_type": "int"},
        {"name": "j_id", "field_type": "int"},
        {"name": "country_id", "field_type": "int", "index_type": "tree"},
        {"name": "code", "field_type": "int", "index_type": "tree"},
    ])
    countries = create_ns("countries", [
        {"is_pk": True, "name": "id", "field_type": "int"},
        {"name": "j_id", "field_type": "int"},
        {"name": "active", "field_type": "bool", "index_type": "-"},
    ])
    archive = create_ns("archive", [
        {"is_pk": True, "name": "id", "field_type": "int"},
        {"name": "author_id", "field_type": "int", "index_type": "tree"},
        {"name": "year", "field_type": "int", "index_type": "tree"},
    ])
    nss = {
        "books": books,
        "authors": authors,
        "locations": locations,
        "countries": countries,
        "archive": archive
    }
    yield nss
    for ns in nss:
        db.namespace.drop(ns)


@pytest.fixture(scope="class")
def nested_join_items(db, nested_join_nss):
    items = {
        "books": [
            {"id": 1, "author_id": 10, "price": 20},
            {"id": 2, "author_id": 20, "price": 25},
            {"id": 3, "author_id": 999, "price": 30},
            {"id": 4, "author_id": 30, "price": 5},
            {"id": 5, "author_id": 40, "price": 15},
            {"id": 6, "author_id": 10, "price": 40},
            {"id": 7, "author_id": 10, "price": 50},
            {"id": 8, "author_id": 888, "price": 100},
            {"id": 9, "author_id": 50, "price": 35},
        ],
        "authors": [
            {"id": 10, "j_id": 10, "location_id": 100, "age": 55},
            {"id": 11, "j_id": 10, "location_id": 200, "age": 56},
            {"id": 20, "j_id": 20, "location_id": 200, "age": 42},
            {"id": 30, "j_id": 30, "location_id": 999, "age": 35},
            {"id": 40, "j_id": 40, "location_id": 400, "age": 60},
            {"id": 50, "j_id": 50, "location_id": 50, "age": 28},
        ],
        "locations": [
            {"id": 50, "j_id": 50, "country_id": 1, "code": 7},
            {"id": 100, "j_id": 100, "country_id": 1, "code": 11},
            {"id": 150, "j_id": 100, "country_id": 2, "code": 19},
            {"id": 200, "j_id": 200, "country_id": 2, "code": 50},
            {"id": 250, "j_id": 200, "country_id": 3, "code": 30},
            {"id": 400, "j_id": 400, "country_id": 10, "code": 100},
            {"id": 300, "j_id": 300, "country_id": 1, "code": 0},
        ],
        "countries": [
            {"id": 1, "j_id": 1, "active": True},
            {"id": 2, "j_id": 1, "active": False},
            {"id": 3, "j_id": 2, "active": True},
            {"id": 4, "j_id": 3, "active": False},
            {"id": 10, "j_id": 10, "active": True},
            {"id": 11, "j_id": 10, "active": True},
            {"id": 20, "j_id": 20, "active": True},
            {"id": 777, "j_id": 777, "active": True},
        ],
        "archive": [
            {"id": 100, "author_id": 10, "year": 30},
            {"id": 200, "author_id": 30, "year": 30},
            {"id": 300, "author_id": 20, "year": 1},
        ]
    }
    for ns, items_list in items.items():
        create_items(db, ns, items_list)
    return items

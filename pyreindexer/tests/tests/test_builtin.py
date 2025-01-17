import shutil

import pytest

from tests.helpers.api import ConnectorApi
from tests.helpers.base_helper import prepare_ns_with_items


CONNECTIONS = []


@pytest.fixture
def db(request):
    if request.config.getoption('--mode') != "builtin":
        pytest.skip("tests only for builtin mode")

    def _inner(**kwargs):
        db = ConnectorApi("builtin://tmp/test_db", **kwargs)
        CONNECTIONS.append(db)
        return db

    yield _inner


@pytest.fixture(autouse=True)
def clear_storage(db):
    yield
    for conn in CONNECTIONS:
        conn.close()
    CONNECTIONS.clear()
    shutil.rmtree("tmp/", ignore_errors=True)


class TestBuiltinOptions:
    def test_builtin_options(self, db):
        db = db(max_replication_updates_size=1, allocator_cache_limit=1, allocator_cache_part=1)
        prepare_ns_with_items(db)

    def test_builtin_options_zero_values(self, db):
        db = db(max_replication_updates_size=0, allocator_cache_limit=0, allocator_cache_part=0)
        prepare_ns_with_items(db)

    def test_builtin_options_negative_values(self, db):
        db = db(max_replication_updates_size=-1000, allocator_cache_limit=-1000, allocator_cache_part=-1000)
        prepare_ns_with_items(db)

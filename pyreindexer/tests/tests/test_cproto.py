import shutil
from datetime import timedelta

import pytest
from hamcrest import *

from tests.helpers.api import ConnectorApi
from tests.helpers.base_helper import prepare_ns_with_items


CONNECTIONS = []


@pytest.fixture
def db(request):
    if request.config.getoption('--mode') != "cproto":
        pytest.skip("tests only for cproto mode")

    def _inner(**kwargs):
        db = ConnectorApi("cproto://127.0.0.1:6534/test_db", **kwargs)
        CONNECTIONS.append(db)
        return db

    yield _inner


@pytest.fixture(autouse=True)
def clear_storage(db):
    yield
    for db in CONNECTIONS:
        for ns in db.namespace.enumerate():
            if not ns["name"].startswith("#"):
                db.namespace.drop(ns["name"])
        db.close()
    CONNECTIONS.clear()
    shutil.rmtree("tmp/", ignore_errors=True)


class TestCprotoOptions:
    def test_cproto_options(self, db):
        db = db(fetch_amount=10, reconnect_attempts=1, net_timeout=timedelta(milliseconds=1000),
                enable_compression=True, start_special_thread=True, client_name="qa_tests", sync_rxcoro_count=1)
        prepare_ns_with_items(db)

    def test_cproto_options_zero_values(self, db):
        db = db(reconnect_attempts=0, net_timeout=timedelta(milliseconds=0), sync_rxcoro_count=0)
        ns_name = "test_zero_val"
        items = prepare_ns_with_items(db, ns_name)
        query = f"SELECT * FROM {ns_name}"
        result = list(db.query.sql(query))
        assert_that(result, equal_to(items))

    def test_cproto_options_fetch_amount_zero_value(self, db):
        assert_that(calling(db).with_args(fetch_amount=0),
                    raises(ValueError, pattern="'fetch_amount' must be greater than zero"))

    def test_cproto_options_negative_values(self, db):
        db = db(reconnect_attempts=-1, net_timeout=timedelta(milliseconds=-1), sync_rxcoro_count=-1)
        ns_name = "test_negative_val"
        items = prepare_ns_with_items(db, ns_name)
        query = f"SELECT * FROM {ns_name}"
        result = list(db.query.sql(query))
        assert_that(result, equal_to(items))

    def test_cproto_fetch_amount(self, db):
        """ Check that fetch amount doesn't affect the amount of total items returned """
        db = db(fetch_amount=1)
        ns_name = "test_fetch"
        items = prepare_ns_with_items(db, ns_name)
        query = f"SELECT * FROM {ns_name}"
        result = list(db.query.sql(query))
        assert_that(result, equal_to(items))

# import shutil
# from datetime import timedelta
#
# import pytest
# from hamcrest import *
#
# from pyreindexer.query import CondType
# from tests.helpers.api import ConnectorApi
# from tests.helpers.base_helper import get_ns_items
# from tests.test_data.constants import item_definition
#
#
# @pytest.fixture(scope="module")
# def db(request):
#     """
#     Create a database
#     """
#     if request.config.getoption("--mode") == "builtin":
#         pytest.skip("auth test is only for cproto mode")
#
#     db = ConnectorApi("cproto://rxuser:rxpass@127.0.0.1:6535/test_db")
#     yield db
#     db.close()
#     shutil.rmtree("tmp/", ignore_errors=True)
#
#
# class TestAuth:
#     def test_auth_sql_select(self, db, namespace, index, item):
#         # Given("Create namespace with id and item")
#         # When ("Execute SQL query SELECT")
#         query = f"SELECT * FROM {namespace}"
#         items_list = list(db.query.sql(query))
#         # Then ("Check that selected item is in result")
#         assert_that(items_list, equal_to([item]))
#
#     def test_auth_query_select_where(self, db, namespace, index, items):
#         # Given("Create namespace with index and items")
#         # Given ("Create new query")
#         query = db.query.new(namespace)
#         # When ("Make select query")
#         query_result = list(query.where("id", CondType.CondEq, 3).execute(timeout=timedelta(seconds=1)))
#         # Then ("Check that selected item is in result")
#         assert_that(query_result, equal_to([items[3]]))
#
#     def test_auth_tx_item_insert(self, db, namespace, index):
#         # Given("Create namespace with index")
#         # When ("Insert item into namespace via tx")
#         transaction = db.tx.begin(namespace)
#         transaction.insert_item(item_definition)
#         transaction.commit(timeout=timedelta(milliseconds=1000))
#         # Then ("Check that item was added")
#         select_result = get_ns_items(db, namespace)
#         assert_that(select_result, equal_to([item_definition]))

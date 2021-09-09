from hamcrest import *

from qa_test.helpers.sql import sql_query


class TestSqlQueries:
    def test_sql_select(self, namespace, index, item):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        item_definition = item
        # When ("Execute SQL query SELECT")
        query = f'SELECT * FROM {namespace_name}'
        item_list = sql_query(namespace, query)
        # Then ("Check that selected item is in result")
        assert_that(item_list, has_item(equal_to(item_definition)), "Can't SQL select data")

    def test_sql_update(self, namespace, index, item):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        # When ("Execute SQL query UPDATE")
        query = f"UPDATE {namespace_name} SET 'val' = 'new_val' WHERE id = 100"
        item_list = sql_query(namespace, query)
        # Then ("Check that item is updated")
        assert_that(item_list, has_item(equal_to({'id': 100, 'val': 'new_val'})), "Can't SQL update data")

    def test_sql_delete(self, namespace, index, item):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        # When ("Execute SQL query DELETE")
        query_delete = f"DELETE FROM {namespace_name} WHERE id = 100"
        sql_query(namespace, query_delete)
        # Then ("Check that item is deleted")
        query_select = f"SELECT * FROM {namespace_name}"
        item_list = sql_query(namespace, query_select)
        assert_that(item_list, equal_to([]), "Can't SQL delete data")

from hamcrest import *

from tests.helpers.sql import sql_query


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

    def test_sql_select_with_join(self, namespace, second_namespace_for_join, index, items):
        # Given("Create two namespaces")
        db, namespace_name = namespace
        second_namespace_name, second_ns_item_definition_join = second_namespace_for_join
        # When ("Execute SQL query SELECT with JOIN")
        query = f'SELECT id FROM {namespace_name} INNER JOIN {second_namespace_name} ON {namespace_name}.id = {second_namespace_name}.id'
        item_list = sql_query(namespace, query)
        # Then ("Check that selected item is in result")
        assert_that(item_list,
                    has_item(equal_to({'id': 1, f'joined_{second_namespace_name}': [second_ns_item_definition_join]})),
                    "Can't SQL select data with JOIN")

    def test_sql_select_with_condition(self, namespace, index, items):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        # When ("Execute SQL query SELECT")
        query = f'SELECT * FROM {namespace_name} WHERE id=3'
        item_list = sql_query(namespace, query)
        # Then ("Check that selected item is in result")
        assert_that(item_list, has_item(equal_to({'id': 3, 'val': 'testval3'})), "Can't SQL select data with condition")

    def test_sql_update(self, namespace, index, item):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        # When ("Execute SQL query UPDATE")
        query = f"UPDATE {namespace_name} SET \"val\" = 'new_val' WHERE id = 100"
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

    def test_sql_select_with_syntax_error(self, namespace, index, item):
        # Given("Create namespace with item")
        # When ("Execute SQL query SELECT with incorrect syntax")
        query = f'SELECT *'
        # Then ("Check that selected item is in result")
        assert_that(calling(sql_query).with_args(namespace, query),
                    raises(Exception, matching=has_string(string_contains_in_order(
                        "Expected", "but found"))), "Error wasn't raised when syntax was incorrect")

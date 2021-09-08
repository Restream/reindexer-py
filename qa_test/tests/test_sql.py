from hamcrest import *

from qa_test.helpers.sql import select_query


class TestSqlQueries:
    def test_sql_select(self, namespace, index, item):
        db, namespace_name = namespace
        item_definition = item
        query = f'SELECT * FROM {namespace_name}'
        item_list = select_query(namespace, query)
        assert_that(item_list, has_item(equal_to(item_definition)), "Can't SQL select data")

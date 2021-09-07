from hamcrest import *


class TestSqlQueries:
    def test_sql_select(self, namespace, index, item):
        db, namespace_name = namespace
        item_definition = item
        item_list = list(db.select(f'SELECT * FROM {namespace_name}'))
        print(item_list)
        assert_that(item_list, has_item(equal_to(item_definition)), "Can't SQL select data")

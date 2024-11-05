from hamcrest import *

from ..helpers.sql import sql_query


class TestSqlQueries:
    def test_sql_select(self, namespace, index, item):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        # When ("Execute SQL query SELECT")
        query = f"SELECT * FROM {namespace_name}"
        items_list = sql_query(namespace, query)
        # Then ("Check that selected item is in result")
        assert_that(items_list, equal_to([item]), "Can't SQL select data")

    def test_sql_select_with_join(self, namespace, second_namespace_for_join, index, items):
        # Given("Create two namespaces")
        db, namespace_name = namespace
        second_namespace_name, second_ns_item_definition_join = second_namespace_for_join
        # When ("Execute SQL query SELECT with JOIN")
        query = f"SELECT id FROM {namespace_name} INNER JOIN {second_namespace_name} " \
                f"ON {namespace_name}.id = {second_namespace_name}.id"
        item_list = sql_query(namespace, query)
        # Then ("Check that selected item is in result")
        assert_that(item_list,
                    has_item(equal_to({'id': 1, f'joined_{second_namespace_name}': [second_ns_item_definition_join]})),
                    "Can't SQL select data with JOIN")

    def test_sql_select_with_condition(self, namespace, index, items):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        # When ("Execute SQL query SELECT")
        item_id = 3
        query = f"SELECT * FROM {namespace_name} WHERE id = {item_id}"
        items_list = sql_query(namespace, query)
        # Then ("Check that selected item is in result")
        assert_that(items_list, equal_to([items[item_id]]), "Can't SQL select data with condition")

    def test_sql_update(self, namespace, index, item):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        # When ("Execute SQL query UPDATE")
        item["val"] = "new_val"
        query = f"UPDATE {namespace_name} SET \"val\" = '{item['val']}' WHERE id = 100"
        items_list = sql_query(namespace, query)
        # Then ("Check that item is updated")
        assert_that(items_list, equal_to([item]), "Can't SQL update data")

    def test_sql_delete(self, namespace, index, item):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        # When ("Execute SQL query DELETE")
        query_delete = f"DELETE FROM {namespace_name} WHERE id = 100"
        sql_query(namespace, query_delete)
        # Then ("Check that item is deleted")
        query_select = f"SELECT * FROM {namespace_name}"
        item_list = sql_query(namespace, query_select)
        assert_that(item_list, empty(), "Can't SQL delete data")

    def test_sql_select_with_syntax_error(self, namespace, index, item):
        # Given("Create namespace with item")
        # When ("Execute SQL query SELECT with incorrect syntax")
        query = "SELECT *"
        # Then ("Check that selected item is in result")
        assert_that(calling(sql_query).with_args(namespace, query),
                    raises(Exception, pattern="Expected .* but found"),
                    "Error wasn't raised when syntax was incorrect")

    def test_sql_select_with_aggregations(self, namespace, index, items):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        # When ("Insert items into namespace")
        for _ in range(5):
            db.item_insert(namespace_name, {"id": 100}, ["id=serial()"])

        select_result = db.select(f"SELECT min(id), max(id), avg(id), sum(id) FROM {namespace_name}").get_agg_results()
        assert_that(select_result, has_length(4), "The aggregation result does not contain all aggregations")

        ids = [i["id"] for i in items]
        expected_values = {"min": min(ids), "max": max(ids), "avg": sum(ids) / len(items), "sum": sum(ids)}

        # Then ("Check that returned agg results are correct")
        for agg in select_result:
            assert_that(agg['value'], equal_to(expected_values[agg['type']]),
                        f"Incorrect aggregation result for {agg['type']}")

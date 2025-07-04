import copy
from datetime import timedelta
from typing import Final

from hamcrest import *

from pyreindexer.exceptions import ApiError
from tests.helpers.base_helper import random_vector
from tests.helpers.check_helper import check_response_has_close_to_ns_items
from tests.test_data.constants import vector_index_bf, vector_index_hnsw, vector_index_ivf


class TestSqlQueries:
    def test_sql_select(self, db, namespace, index, item):
        # Given("Create namespace with item")
        # When ("Execute SQL query SELECT")
        query = f"SELECT * FROM {namespace}"
        items_list = list(db.query.sql(query, timeout=timedelta(milliseconds=1000)))
        # Then ("Check that selected item is in result")
        assert_that(items_list, equal_to([item]), "Can't SQL select data")

    def test_sql_select_with_join(self, db, namespace, index, items, second_namespace, second_item):
        # Given("Create two namespaces")
        # When ("Execute SQL query SELECT with JOIN")
        query = f"SELECT id FROM {namespace} INNER JOIN {second_namespace} " \
                f"ON {namespace}.id = {second_namespace}.id"
        item_list = list(db.query.sql(query))
        # Then ("Check that selected item is in result")
        item_with_joined = {'id': 1, f'joined_{second_namespace}': [second_item]}
        assert_that(item_list, equal_to([item_with_joined]),
                    "Can't SQL select data with JOIN")

    def test_sql_select_with_condition(self, db, namespace, index, items):
        # Given("Create namespace with item")
        # When ("Execute SQL query SELECT")
        item_id = 3
        query = f"SELECT * FROM {namespace} WHERE id = {item_id}"
        items_list = list(db.query.sql(query))
        # Then ("Check that selected item is in result")
        assert_that(items_list, equal_to([items[item_id]]), "Can't SQL select data with condition")

    def test_sql_update(self, db, namespace, index, item):
        # Given("Create namespace with item")
        # When ("Execute SQL query UPDATE")
        item["val"] = "new_val"
        query = f"UPDATE {namespace} SET \"val\" = '{item['val']}' WHERE id = 100"
        items_list = list(db.query.sql(query))
        # Then ("Check that item is updated")
        assert_that(items_list, equal_to([item]), "Can't SQL update data")

    def test_sql_delete(self, db, namespace, index, item):
        # Given("Create namespace with item")
        # When ("Execute SQL query DELETE")
        query_delete = f"DELETE FROM {namespace} WHERE id = 100"
        db.query.sql(query_delete)
        # Then ("Check that item is deleted")
        query_select = f"SELECT * FROM {namespace}"
        item_list = list(db.query.sql(query_select))
        assert_that(item_list, empty(), "Can't SQL delete data")

    def test_sql_select_with_syntax_error(self, db, namespace, index, item):
        # Given("Create namespace with item")
        # When ("Execute SQL query SELECT with incorrect syntax")
        query = "SELECT *"
        # Then ("Check that selected item is in result")
        assert_that(calling(db.query.sql).with_args(query),
                    raises(ApiError, pattern="Expected .* but found"),
                    "Error wasn't raised when syntax was incorrect")

    def test_sql_select_with_aggregations(self, db, namespace, index, items):
        # Given("Create namespace with item")
        # When ("Insert items into namespace")
        select_result = db.query.sql(f"SELECT min(id), max(id), avg(id), sum(id) FROM {namespace}").get_agg_results()
        assert_that(select_result, has_length(4), "The aggregation result does not contain all aggregations")

        ids = [i["id"] for i in items]
        expected_values = {"min": min(ids), "max": max(ids), "avg": sum(ids) / len(items), "sum": sum(ids)}

        # Then ("Check that returned agg results are correct")
        for agg in select_result:
            assert_that(agg['value'], equal_to(expected_values[agg['type']]),
                        f"Incorrect aggregation result for {agg['type']}")

    def test_sql_select_timeout_small(self, db, namespace, index):
        # Given("Create namespace with items")
        items = [{"id": i, "val": f"testval{i}", "non_idx": i + 1} for i in range(10000)]
        for item in items:
            db.item.insert("new_ns", item)
        # When ("Try to execute SQL query SELECT with small timeout")
        query = ("SELECT * FROM new_ns WHERE id > -1 AND non_idx > 0 MERGE "
                 "(SELECT * FROM new_ns WHERE val < 'testval1000' AND non_idx > 0) MERGE "
                 "(SELECT * FROM new_ns WHERE val > 'testval1000' AND id RANGE(1,9000) AND non_idx > 100) MERGE "
                 "(SELECT * FROM new_ns WHERE non_idx > id AND NOT (id < 100))")
        assert_that(calling(db.query.sql).with_args(query, timeout=timedelta(milliseconds=1)),
                    raises(ApiError, pattern="Context timeout|Read lock (.*) was canceled or timed out (mutex)"))


class TestSqlQueriesKNN:

    def test_sql_select_knn_brute_force(self, db, namespace, index):
        # Given ("Create float vector index")
        dimension: Final[int] = 8
        index = copy.deepcopy(vector_index_bf)
        index["config"] = {"dimension": dimension, "metric": "l2", "start_size": 1000}
        db.index.create(namespace, index)
        # Given("Insert items")
        items = [{"id": i, "vec": random_vector(dimension)} for i in range(100)]
        for item in items:
            db.item.insert("new_ns", item)
        # When ("Execute SQL query SELECT KNN")
        value = random_vector(dimension)
        k = 47
        query = f"SELECT *, vectors() FROM {namespace} WHERE KNN(vec, {value}, k={k})"
        query_result = list(db.query.sql(query, timeout=timedelta(seconds=1)))
        # Then ("Check knn select result")
        check_response_has_close_to_ns_items(query_result, items)
        assert_that(query_result, has_length(k))

    def test_sql_select_knn_hnsw(self, db, namespace, index):
        # Given ("Create float vector index")
        dimension: Final[int] = 8
        index = copy.deepcopy(vector_index_hnsw)
        index["config"] = {"dimension": dimension, "metric": "inner_product", "start_size": 1000, "m": 16,
                           "ef_construction": 200}
        db.index.create(namespace, index)
        # Given("Insert items")
        items = [{"id": i, "vec": random_vector(dimension)} for i in range(100)]
        for item in items:
            db.item.insert("new_ns", item)
        # When ("Execute SQL query SELECT KNN")
        value = random_vector(dimension)
        query = f"SELECT *, vectors() FROM {namespace} WHERE KNN(vec, {value}, k=20, ef=30)"
        query_result = list(db.query.sql(query, timeout=timedelta(seconds=1)))
        # Then ("Check knn select result")
        check_response_has_close_to_ns_items(query_result, items)

    def test_sql_select_knn_ivf(self, db, namespace, index):
        # Given ("Create float vector index")
        dimension: Final[int] = 8
        index = copy.deepcopy(vector_index_ivf)
        index["config"] = {"dimension": dimension, "metric": "l2", "centroids_count": 3}
        db.index.create(namespace, index)
        # Given("Insert items")
        items = [{"id": i, "vec": random_vector(dimension)} for i in range(150)]
        for item in items:
            db.item.insert("new_ns", item)
        # When ("Execute SQL query SELECT KNN")
        value = random_vector(dimension)
        query = f"SELECT *, vectors() FROM {namespace} WHERE KNN(vec, {value}, k=30, nprobe=2)"
        query_result = list(db.query.sql(query, timeout=timedelta(seconds=1)))
        # Then ("Check knn select result")
        check_response_has_close_to_ns_items(query_result, items)

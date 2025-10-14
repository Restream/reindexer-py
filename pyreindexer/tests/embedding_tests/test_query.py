import copy
from typing import Final

import pytest
from hamcrest import *

from pyreindexer.exceptions import ApiError, QueryError
from pyreindexer.index_search_params import IndexSearchParamBruteForce, IndexSearchParamHnsw, IndexSearchParamIvf
from tests.helpers.base_helper import random_vector
from tests.helpers.check_helper import check_response_has_close_to_ns_items
from tests.test_data.constants import vector_index_bf, vector_index_hnsw, vector_index_ivf


class TestQueryWhereKNNString:

    def test_query_where_knn_string_bf(self, db, namespace, index):
        # Given ("Create float vector index")
        dimension: Final[int] = 5
        index = copy.deepcopy(vector_index_bf)
        index["config"]["dimension"] = dimension
        index["config"]["embedding"] = {
            "query_embedder": {"URL": "http://127.0.0.1:8000"}
        }
        db.index.create(namespace, index)
        # Given("Insert items")
        items = [{"id": i, "vec": random_vector(dimension)} for i in range(10)]
        for item in items:
            db.item.insert("new_ns", item)
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Execute query")
        k: Final[int] = 5
        param = IndexSearchParamBruteForce(k=k)
        query_result = list(
            query.where_knn_string("vec", "word", param)
            .select_fields("vectors()")
            .execute())
        # Then ("Check knn select result")
        check_response_has_close_to_ns_items(query_result, items)
        assert_that(query_result, has_length(k))

    def test_query_where_knn_string_hnsw(self, db, namespace, index):
        # Given ("Create float vector index")
        dimension: Final[int] = 5
        index = copy.deepcopy(vector_index_hnsw)
        index["config"]["dimension"] = dimension
        index["config"]["embedding"] = {
            "query_embedder": {"URL": "http://127.0.0.1:8000"}
        }
        db.index.create(namespace, index)
        # Given("Insert items")
        items = [{"id": i, "vec": random_vector(dimension)} for i in range(10)]
        for item in items:
            db.item.insert("new_ns", item)
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Execute query")
        param = IndexSearchParamHnsw(k=5, ef=5)
        query_result = list(
            query.where_knn_string("vec", "same same", param)
            .select_fields("vectors()")
            .execute())
        # Then ("Check knn select result")
        check_response_has_close_to_ns_items(query_result, items)

    def test_query_where_knn_string_ivf(self, db, namespace, index):
        # Given ("Create float vector index")
        dimension: Final[int] = 5
        index = copy.deepcopy(vector_index_ivf)
        index["config"]["dimension"] = dimension
        index["config"]["embedding"] = {
            "query_embedder": {"URL": "http://127.0.0.1:8000"}
        }
        db.index.create(namespace, index)
        # Given("Insert items")
        items = [{"id": i, "vec": random_vector(dimension)} for i in range(10)]
        for item in items:
            db.item.insert("new_ns", item)
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Execute query")
        param = IndexSearchParamIvf(k=5, nprobe=2)
        query_result = list(
            query.where_knn_string("vec", "a b c", param)
            .select_fields("vectors()")
            .execute())
        # Then ("Check knn select result")
        check_response_has_close_to_ns_items(query_result, items)

    @pytest.mark.parametrize("value, err_type, err_msg", [
        (None, TypeError, "object of type 'NoneType' has no len()"),
        (1, TypeError, "object of type 'int' has no len()"),
        (["abc"], TypeError, "must be str, not list"),
        ({"a": "b"}, TypeError, "must be str, not dict"),
        ("", QueryError, "A required parameter is not specified. `value` can't be None or empty"),
    ])
    def test_query_where_knn_string_invalid_value(self, db, namespace, index, value, err_type, err_msg):
        # Given ("Create float vector index")
        dimension: Final[int] = 5
        index = copy.deepcopy(vector_index_hnsw)
        index["config"]["dimension"] = dimension
        index["config"]["embedding"] = {
            "query_embedder": {"URL": "http://127.0.0.1:8000"}
        }
        db.index.create(namespace, index)
        # Given("Insert items")
        items = [{"id": i, "vec": random_vector(dimension)} for i in range(10)]
        for item in items:
            db.item.insert("new_ns", item)
        # Given ("Create new query")
        param = IndexSearchParamHnsw(k=5, ef=5)
        query = db.query.new(namespace).select_fields("vectors()")
        # When ("Try to add where_knn_string to the query")
        assert_that(calling(query.where_knn_string).with_args("vec", value, param),
                    raises(err_type, pattern=err_msg))

    def test_query_where_knn_string_no_query_embedder_config(self, db, namespace, index):
        # Given ("Create float vector index")
        dimension: Final[int] = 5
        index = copy.deepcopy(vector_index_hnsw)
        index["config"]["dimension"] = dimension
        db.index.create(namespace, index)
        # Given("Insert items")
        items = [{"id": i, "vec": random_vector(dimension)} for i in range(10)]
        for item in items:
            db.item.insert("new_ns", item)
        # Given ("Create new query")
        param = IndexSearchParamHnsw(k=5, ef=5)
        query = db.query.new(namespace).where_knn_string("vec", "word", param).select_fields("vectors()")
        # When ("Try to execute query without query_embedder")
        param = IndexSearchParamHnsw(k=5, ef=5)
        query = query.where_knn_string("vec", "word", param).select_fields("vectors()")
        err_msg = ("Failed to get embedding for 'vec'. Problem with client: Unexpected problem with client|"
                   "Trying to find knn by string. No Embedder configured for index 'vec'")
        assert_that(calling(query.execute).with_args(), raises(ApiError, pattern=err_msg))

import pytest
from hamcrest import *

from point import Point
from query import CondType
from tests.test_data.constants import AGGREGATE_FUNCTIONS_MATH


class TestQuerySelect:
    def test_query_select_where(self, db, namespace, index, items):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query")
        query_result = list(query.where("id", CondType.CondEq, 3).execute())
        # Then ("Check that selected item is in result")
        assert_that(query_result, equal_to([items[3]]), "Wrong query results")

    def test_query_select_fields(self, db, namespace, index, items):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with select fields")
        select_result = list(query.select(["id"]).must_execute())
        # Then ("Check that selected items are in result")
        ids = [{"id": i["id"]} for i in items]
        assert_that(select_result, equal_to(ids), "Wrong query results")

    # TODO ??? build query
    def test_query_select_where_query(self, db, namespace, index, items):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        # query = db.query.new(namespace).where("id", CondType.CondLt, 5)
        # sub_query = db.query.new(namespace).where("id", CondType.CondGt, 0)
        query = db.query.new(namespace)
        sub_query = db.query.new(namespace)
        # When ("Make select query with where_query subquery")
        query_result = list(query.where_query(sub_query, CondType.CondEq, 1).execute())
        # Then ("Check that selected item is in result")
        assert_that(query_result, equal_to([items[1]]), "Wrong query results")

    # TODO ??? build query
    def test_query_select_where_composite(self, db, namespace, composite_index, items):
        # Given("Create namespace with composite index")
        # Given ("Create new query")
        query = db.query.new(namespace)
        query_comp = db.query.new(namespace).where("id", CondType.CondEq, 1).where("val", CondType.CondEq, "testval1")
        # When ("Make select query with where_composite")
        query_result = list(query.where_composite("comp_idx", CondType.CondEq, query_comp).execute())
        # Then ("Check that selected item is in result")
        assert_that(query_result, equal_to([items[1]]), "Wrong query results")

    def test_query_select_where_uuid(self, db, namespace, index):
        # Given("Create namespace with index")
        # Given ("Create uuid index")
        db.index.create(namespace, {"name": "uuid", "json_paths": ["uuid"], "field_type": "uuid", "index_type": "hash"})
        # Given ("Create items")
        items = [{"id": 0, "uuid": "f0dbda48-1b92-4aa1-b4dc-39b6867a202e"},
                 {"id": 1, "uuid": "189005c5-106f-4582-9838-f7a5b18649fc"},
                 {"id": 2, "uuid": "50005725-dd9d-4891-a9bc-7c7cb0ed2a3d"}]
        for item in items:
            db.item.insert(namespace, item)
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with where_uuid")
        item = items[1]
        query_result = list(query.where_uuid("uuid", CondType.CondEq, [item["uuid"]]).execute())
        # Then ("Check that selected item is in result")
        assert_that(query_result, equal_to([item]), "Wrong query results")

    def test_query_select_where_between_fields(self, db, namespace, index):
        # Given("Create namespace with index")
        # Given("Create items")
        items = [{"id": 0, "age": 0.5}, {"id": 1, "age": 1}, {"id": 2, "age": 20}]
        for item in items:
            db.item.insert(namespace, item)
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with where_between_fields")
        query_result = list(query.where_between_fields("id", CondType.CondEq, "age").execute())
        # Then ("Check that selected item is in result")
        assert_that(query_result, equal_to([items[1]]), "Wrong query results")

    def test_query_select_with_brackets_and_ops(self, db, namespace, index, items):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with brackets and different op")
        query = (query.where("id", CondType.CondEq, 0)
                 .op_or().open_bracket()
                 .op_and().where("id", CondType.CondGe, 2)
                 .op_or().where("id", CondType.CondLt, 7)
                 .op_not().where("id", CondType.CondSet, [1, 6])

                 .op_and().open_bracket()
                 .op_not().where("id", CondType.CondRange, [5, 9])
                 .close_bracket()

                 .close_bracket())
        query_result = list(query.execute())
        # Then ("Check that selected items are in result")
        expected_items = [items[i] for i in [0, 2, 3, 4]]
        assert_that(query_result, equal_to(expected_items), "Wrong query results")

    def test_query_select_match(self, db, namespace, index, items):
        # Given("Create namespace with index and items")
        # Given ("Create string index")
        db.index.create(namespace, {"name": "val", "json_paths": ["val"], "field_type": "string", "index_type": "hash"})
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with match")
        query_result = list(query.match("val", ["testval1"]).execute())
        # Then ("Check that selected item is in result")
        assert_that(query_result, equal_to([items[1]]), "Wrong query results")

        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with match and empty result")
        query_result = list(query.match("val", ["testval"]).execute())
        # Then ("Check that result is empty")
        assert_that(query_result, empty(), "Wrong query results")

    # TODO fix 'Process finished with exit code 139 (interrupted by signal 11:SIGSEGV)'
    def test_query_select_dwithin(self, db, namespace, index, rtree_index_and_items):
        # Given("Create namespace with rtree index and items")
        items = rtree_index_and_items
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with dwithin")
        query_result = list(query.dwithin("rtree", Point(3, 2.5), 1.5).execute())
        # Then ("Check that selected item is in result")
        expected_items = [items[i] for i in [1, 2, 3]]  # TODO change expected after err fix
        assert_that(query_result, equal_to(expected_items), "Wrong query results")

    def test_query_select_limit_offset(self, db, namespace, index, items):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with limit and offset")
        query_result = list(query.limit(3).offset(1).execute())
        # Then ("Check that selected items are in result")
        expected_items = [items[i] for i in [1, 2, 3]]
        assert_that(query_result, equal_to(expected_items), "Wrong query results")

    # TODO ??? get explain results
    def test_query_select_explain(self, db, namespace, index, items):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with explain")
        query_result = query.explain().execute()
        # Then ("Check that selected items are in result")
        assert_that(list(query_result), equal_to(items), "Wrong query results")
        # Then ("Check that explain is in result")
        assert_that(query_result, equal_to(1), "There is no explain in query results")


class TestQuerySelectAggregations:
    @pytest.mark.parametrize("calculate, function_name", AGGREGATE_FUNCTIONS_MATH)
    def test_query_select_aggregations_math(self, db, namespace, index, items, calculate, function_name):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        aggregation_query = getattr(query, function_name)
        # When ("Make select query")
        query_result = aggregation_query("id").execute()
        # Then ("Check that selected item is in result")
        assert_that(list(query_result), empty(), "Wrong query results")
        # Then ("Check aggregation results")
        ids_list = list(range(len(items)))
        assert_that(query_result.get_agg_results(),
                    equal_to([{"value": calculate(ids_list), "type": function_name.split("_")[-1], "fields": ["id"]}]),
                    "Wrong aggregation results")

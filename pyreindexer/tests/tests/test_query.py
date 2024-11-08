import pytest
from hamcrest import *

from point import Point
from query import CondType, StrictMode
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

    def test_query_select_get_true(self, db, namespace, index, items):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with get")
        query_result = list(query.get())
        # Then ("Check that selected item is in result")
        assert_that(query_result, equal_to([items[0], True]), "Wrong query results")

    def test_query_select_get_false(self, db, namespace, index, items):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with get")
        query_result = list(query.where("id", CondType.CondEq, 99).get())
        # Then ("Check that selected item is in result")
        assert_that(query_result, equal_to(["", False]), "Wrong query results")

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

    def test_query_select_equal_position(self, db, namespace, index, array_indexes_and_items):
        # Given("Create namespace with array indexes and items")
        items = array_indexes_and_items
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with equal_position")
        query.where("arr1", CondType.CondEq, 1).where("arr2", CondType.CondEq, 1)
        query_result = list(query.equal_position(["arr1", "arr2"]).execute())
        # Then ("Check that selected item is in result")
        assert_that(query_result, equal_to([items[1]]), "Wrong query results")

    def test_query_select_limit_offset(self, db, namespace, index, items):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with limit and offset")
        query_result = list(query.limit(3).offset(1).execute())
        # Then ("Check that selected items are in result")
        expected_items = [items[i] for i in [1, 2, 3]]
        assert_that(query_result, equal_to(expected_items), "Wrong query results")

    @pytest.mark.parametrize("func_total", ["request_total", "cached_total"])
    def test_query_select_request_total(self, db, namespace, index, items, func_total):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with limit and offset")
        query_result = getattr(query, func_total)("id").execute()
        # Then ("Check that selected items are in result")
        assert_that(list(query_result), equal_to(items), "Wrong query results")
        # Then ("Check that total is in result")
        # TODO: need get_explain_results in query_results
        # assert_that(query_result.get_total_results(), equal_to(""), "There is no total in query results")

    def test_query_select_with_rank(self, db, namespace, index, ft_index_and_items):
        # Given("Create namespace with ft index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query")
        query_result = list(query.where("ft", CondType.CondEq, "word~").with_rank().execute())
        # Then ("Check that selected item is in result with rank")
        for res_item in query_result:
            assert_that(res_item, has_entries("id", is_(int), "ft", is_(str), "rank()", is_(float)),
                        "Wrong query results")

    def test_query_select_functions(self, db, namespace, index, ft_index_and_items):
        # Given("Create namespace with ft index and items")
        ft_index_and_items
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query")
        query.where("ft", CondType.CondEq, "word~")
        query_result = list(query.functions(["ft=highlight(<,>)"]).execute())
        # Then ("Check that selected item is in result and highlighted")
        query_results_ft = [i["ft"] for i in query_result]
        expected_ft_content = ["one <word>", "<sword> two", "three <work> 333"]
        assert_that(query_results_ft, contains_inanyorder(*expected_ft_content), "Wrong query results")

    # TODO self.api.merge(query) takes 4 arguments (but 1 given - query)
    def test_query_select_merge(self, db, namespace, index, items, second_namespace):
        # Given("Create namespace with index and items")
        # Given("Create second namespace with index and items")
        second_ns_name, item2 = second_namespace
        # Given ("Create new query")
        query1 = db.query.new(namespace).where("id", CondType.CondEq, 2)
        # Given ("Create second query")
        query2 = db.query.new(second_ns_name).where("id", CondType.CondEq, 1)
        # When ("Make select query with merge")
        query_result = list(query1.merge(query2).execute())
        # Then ("Check that selected item is in result with merge applied")
        assert_that(query_result, equal_to([items[2], item2]), "Wrong query results")

    def test_query_select_explain(self, db, namespace, index, items):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with explain")
        query_result = query.explain().execute()
        # Then ("Check that selected items are in result")
        assert_that(list(query_result), equal_to(items), "Wrong query results")
        # Then ("Check that explain is in result")
        # TODO: need get_explain_results in query_results
        # assert_that(query_result.get_explain_results(), equal_to(""), "There is no explain in query results")

    # TODO add debug enums
    @pytest.mark.parametrize("debug_level", [StrictMode.NotSet])
    def test_query_select_debug(self, db, namespace, index, items, debug_level):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query")
        query_result = list(query.debug(debug_level).where("id", CondType.CondEq, 1).execute())
        # Then ("Check that selected item is in result")
        assert_that(query_result, equal_to([items[1]]), "Wrong query results")

    @pytest.mark.parametrize("strict_mode", [StrictMode.NotSet, StrictMode.Empty])
    def test_query_select_strict_mode_none_and_empty(self, db, namespace, index, items, strict_mode):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with strict mode")
        query_result = list(query.strict(strict_mode).where("rand", CondType.CondEq, 1).must_execute())
        # Then ("Check that selected item is in result")
        assert_that(query_result, empty(), "Wrong query results")

    # TODO must be err
    def test_query_select_strict_mode_names(self, db, namespace, index, items):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with strict mode")
        query.strict(StrictMode.Names).where("rand", CondType.CondEq, 1)
        err_msg = f"Current query strict mode allows aggregate existing fields only. " \
                  f"There are no fields with name 'rand' in namespace '{namespace}'"
        assert_that(calling(query.must_execute).with_args(),
                    raises(Exception, pattern=err_msg),
                    "Error wasn't raised while strict mode violated")

    # TODO must be err
    def test_query_select_strict_mode_indexes(self, db, namespace, index, items):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with strict mode")
        query.strict(StrictMode.Indexes).where("rand", CondType.CondEq, 1)
        err_msg = f"Current query strict mode allows aggregate index fields only. " \
                  f"There are no indexes with name 'rand' in namespace '{namespace}'"
        assert_that(calling(query.must_execute).with_args(),
                    raises(Exception, pattern=err_msg),
                    "Error wasn't raised while strict mode violated")


class TestQuerySelectAggregations:
    @pytest.mark.parametrize("calculate, aggregate_func", AGGREGATE_FUNCTIONS_MATH)
    def test_query_select_aggregations_math(self, db, namespace, index, items, calculate, aggregate_func):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with aggregations")
        query_result = getattr(query, aggregate_func)("id").execute()
        # Then ("Check that result is empty")
        assert_that(list(query_result), empty(), "Wrong query results")
        # Then ("Check aggregation results")
        ids_list = list(range(len(items)))
        expected_agg_result = [{"value": calculate(ids_list), "type": aggregate_func.split("_")[-1], "fields": ["id"]}]
        assert_that(query_result.get_agg_results(), equal_to(expected_agg_result), "Wrong aggregation results")

    def test_query_select_distinct(self, db, namespace, index, index_and_duplicate_items):
        # Given("Create namespace with index and duplicate items")
        items = index_and_duplicate_items
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with distinct")
        query_result = query.distinct("idx").execute()
        # Then ("Check that only distinct items is in result")
        expected_ids = [0, 1, 3]
        expected_items = [items[i] for i in expected_ids]
        assert_that(list(query_result), equal_to(expected_items), "Wrong query results")
        # Then ("Check aggregation results")
        expected_ids_str = [str(i) for i in expected_ids]
        assert_that(query_result.get_agg_results(),
                    has_item(has_entries(type="distinct", fields=["idx"],
                                         distincts=contains_inanyorder(*expected_ids_str))),
                    "Wrong aggregation results")

    def test_query_select_facet(self, db, namespace, index, index_and_duplicate_items):
        # Given("Create namespace with index and duplicate items")
        items = index_and_duplicate_items
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with facet")
        query.aggregate_facet(["idx"])  # TODO объединить в цепочку?
        query_result = query.execute()
        # Then ("Check that result is empty")
        assert_that(list(query_result), empty(), "Wrong query results")
        # Then ("Check aggregation results")
        expected_facets = [{"count": 1, "values": ["0"]}, {"count": 2, "values": ["1"]}, {"count": 1, "values": ["3"]}]
        assert_that(query_result.get_agg_results(),
                    has_item(has_entries(type="facet", fields=["idx"],
                                         facets=contains_inanyorder(*expected_facets))),
                    "Wrong aggregation results")

    def test_query_select_facet_sort_offset_limit(self, db, namespace, index, index_and_duplicate_items):
        # Given("Create namespace with index and duplicate items")
        items = index_and_duplicate_items
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with facet")
        query.aggregate_facet(["id", "idx"]).sort("id", True).limit(2).offset(1)  # TODO объединить в цепочку?
        query_result = query.execute()
        # Then ("Check that result is empty")
        assert_that(list(query_result), empty(), "Wrong query results")
        # Then ("Check aggregation results")
        expected_facets = [{"count": 1, "values": ["2", "1"]}, {"count": 1, "values": ["1", "1"]}]
        assert_that(query_result.get_agg_results(),
                    has_item(has_entries(type="facet", fields=["id", "idx"],
                                         facets=contains_inanyorder(*expected_facets))),
                    "Wrong aggregation results")


class TestQuerySelectSort:
    @pytest.mark.parametrize("is_reversed", [False, True])
    def test_query_select_sort(self, db, namespace, index, items_shuffled, is_reversed):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with sort")
        query_result = list(query.sort("id", is_reversed).execute())
        # Then ("Check that selected items are sorted")
        expected_items = sorted(items_shuffled, key=lambda x: x["id"], reverse=is_reversed)
        assert_that(query_result, equal_to(expected_items))

    # TODO fix forced_values
    @pytest.mark.parametrize("forced_values, expected_ids", [
        (4, [4, 0, 1, 2, 3]),
        ([1, 3], [1, 3, 0, 2, 4])
    ])
    @pytest.mark.parametrize("is_reversed", [False, True])
    def test_query_select_forced_sort(self, db, namespace, index, items_shuffled, forced_values, expected_ids,
                                      is_reversed):
        # Given("Create namespace with index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with sort")
        query_result = list(query.sort("id", is_reversed, forced_values).execute())  # TODO exit code 255
        # Then ("Check that selected items are sorted")
        expected_items = [items_shuffled[i] for i in expected_ids]
        if is_reversed:
            expected_items.reverse()
        assert_that(query_result, equal_to(expected_items))

    # TODO wip
    @pytest.mark.parametrize("is_reversed", [False, True])
    def test_query_select_sort_stpoint(self, db, namespace, index, rtree_index_and_items, is_reversed):
        # Given("Create namespace with rtree index and items")
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with sort point distance")
        query_result = list(query.sort_stpoint_distance("id", Point(1, 2), is_reversed).execute())
        # Then ("Check that selected items are sorted")
        expected_items = sorted(rtree_index_and_items, key=lambda x: x["id"], reverse=is_reversed)
        assert_that(query_result, equal_to(expected_items))

    # TODO wip
    @pytest.mark.parametrize("is_reversed", [False, True])
    def test_query_select_sort_stfield(self, db, namespace, index, is_reversed):
        # Given("Create namespace with index")
        # Given("Create 2 rtree indexes and items")
        db.index.create(namespace, {"name": "rtree1", "json_paths": ["rtree1"], "field_type": "point",
                                    "index_type": "rtree", "rtree_type": "rstar"})
        db.index.create(namespace, {"name": "rtree2", "json_paths": ["rtree2"], "field_type": "point",
                                    "index_type": "rtree", "rtree_type": "rstar"})
        items = [{"id": i, "rtree1": [i - 1, i + 1], "rtree2": [i + 1, i + 0.5]} for i in range(5)]
        for item in items:
            db.item.insert(namespace, item)
        # Given ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with sort fields distance")
        query_result = list(query.sort_stfield_distance("rtree1", "rtree2", is_reversed).execute())
        # Then ("Check that selected items are sorted")
        expected_items = sorted(items, key=lambda x: x["id"], reverse=is_reversed)
        assert_that(query_result, equal_to(expected_items))


class TestQuerySelectJoin:
    def test_query_select_join(self, db, namespace, index):
        pass

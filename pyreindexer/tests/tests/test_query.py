from hamcrest import *

from query import CondType


class TestQuery:
    def test_query_select_where(self, db, namespace, index, items):
        # Given("Create namespace with index and items")
        # When ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query")
        select_result = list(query.where("id", CondType.CondEq, 3).execute())
        # Then ("Check that selected item is in result")
        assert_that(select_result, has_length(1), "Wrong query results")
        assert_that(select_result, equal_to([items[3]]), "Wrong query results")

    def test_query_select_fields(self, db, namespace, index, items):
        # Given("Create namespace with index and items")
        # When ("Create new query")
        query = db.query.new(namespace)
        # When ("Make select query with select fields")
        select_result = list(query.select(["id"]).must_execute())
        # Then ("Check that selected items is in result")
        ids = [{"id": i["id"]} for i in items]
        assert_that(select_result, equal_to(ids), "Wrong query results")

from datetime import timedelta

from hamcrest import *

from pyreindexer.exceptions import ApiError
from tests.helpers.base_helper import get_ns_description
from tests.test_data.constants import index_definition, updated_index_definition


class TestCrudIndexes:
    def test_initial_namespace_has_no_indexes(self, db, namespace):
        # Given("Create namespace")
        # When ("Get namespace information")
        ns_entry = get_ns_description(db, namespace)
        # Then ("Check that list of indexes in namespace is empty")
        assert_that(ns_entry, has_item(has_entry("indexes", empty())), "Index is not empty")

    def test_create_index(self, db, namespace):
        # Given("Create namespace")
        # When ("Add index")
        db.index.create(namespace, index_definition, timeout=timedelta(milliseconds=1000))
        # Then ("Check that index is added")
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(index_definition))),
                    "Index wasn't created")
        db.index.drop(namespace, 'id', timeout=timedelta(milliseconds=1000))

    def test_update_index(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Update index")
        db.index.update(namespace, updated_index_definition)
        # Then ("Check that index is updated")
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(updated_index_definition))),
                    "Index wasn't updated")

    def test_delete_index(self, db, namespace):
        # Given("Create namespace with index")
        db.index.create(namespace, index_definition)
        # When ("Delete index")
        db.index.drop(namespace, 'id')
        # Then ("Check that index is deleted")
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", empty())), "Index wasn't deleted")

    def test_cannot_add_index_with_same_name(self, db, namespace):
        # Given("Create namespace")
        # When ("Add index")
        db.index.create(namespace, index_definition)
        # Then ("Check that we can't add index with the same name")
        assert_that(calling(db.index.create).with_args(namespace, updated_index_definition),
                    raises(ApiError, pattern="Index '.*' already exists with different settings"),
                    "Index with existing name was created")

    def test_cannot_update_not_existing_index_in_namespace(self, db, namespace):
        # Given ("Create namespace")
        # When ("Update index")
        # Then ("Check that we can't update index that was not created")
        assert_that(calling(db.index.update).with_args(namespace, index_definition),
                    raises(ApiError, pattern=f"Index 'id' not found in '{namespace}'"),
                    "Not existing index was updated")

    def test_cannot_delete_not_existing_index_in_namespace(self, db, namespace):
        # Given ("Create namespace")
        # When ("Delete index")
        # Then ("Check that we can't delete index that was not created")
        index_name = 'id'
        assert_that(calling(db.index.drop).with_args(namespace, index_name),
                    raises(ApiError, pattern=f"Cannot remove index {index_name}: doesn't exist"),
                    "Not existing index was deleted")

    def test_index_update_timeout(self, db, namespace):
        # Given("Create index")
        db.index.create(namespace, index_definition, timeout=timedelta(milliseconds=1000))
        # When ("Update index with big timeout")
        db.index.update(namespace, updated_index_definition, timeout=timedelta(milliseconds=1000))
        # Then ("Check that index is updated")
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(updated_index_definition))),
                    "Index wasn't updated")

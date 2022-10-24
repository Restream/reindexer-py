from hamcrest import *

from tests.helpers.index import *
from tests.helpers.namespace import get_ns_description
from tests.test_data.constants import index_definition, updated_index_definition


class TestCrudIndexes:
    def test_initial_namespace_has_no_indexes(self, database, namespace):
        # Given("Create namespace")
        # When ("Get namespace information")
        ns_entry = get_ns_description(database, namespace)
        # Then ("Check that list of indexes in namespace is empty")
        assert_that(ns_entry, has_item(has_entry("indexes", equal_to([]))),
                    "Index is not empty")

    def test_create_index(self, database, namespace):
        # Given("Create namespace")
        # When ("Add index")
        create_index(namespace, index_definition)
        # Then ("Check that index is added")
        ns_entry = get_ns_description(database, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(equal_to(index_definition)))),
                    "Index wasn't created")
        drop_index(namespace, 'id')

    def test_update_index(self, database, namespace, index):
        # Given("Create namespace with index")
        # When ("Update index")
        update_index(namespace, updated_index_definition)
        # Then ("Check that index is updated")
        ns_entry = get_ns_description(database, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(equal_to(updated_index_definition)))),
                    "Index wasn't updated")

    def test_delete_index(self, database, namespace):
        # Given("Create namespace with index")
        create_index(namespace, index_definition)
        # When ("Delete index")
        drop_index(namespace, 'id')
        # Then ("Check that index is deleted")
        ns_entry = get_ns_description(database, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", equal_to([]))),
                    "Index wasn't deleted")

    def test_cannot_add_index_with_same_name(self, database, namespace):
        # Given("Create namespace")
        # When ("Add index")
        create_index(namespace, index_definition)
        # Then ("Check that we can't add index with the same name")
        assert_that(calling(create_index).with_args(namespace, updated_index_definition),
                    raises(Exception, matching=has_string(string_contains_in_order(
                        "Index", "already exists with different settings"))),
                    "Index with existing name was created")

    def test_cannot_update_not_existing_index_in_namespace(self, database, namespace):
        # Given ("Create namespace")
        db, namespace_name = namespace
        # When ("Update index")
        # Then ("Check that we can't update index that was not created")
        assert_that(calling(update_index).with_args(namespace, index_definition),
                    raises(Exception, matching=has_string(f"Index 'id' not found in '{namespace_name}'")),
                    "Not existing index was updated")

    def test_cannot_delete_not_existing_index_in_namespace(self, database, namespace):
        # Given ("Create namespace")
        # When ("Delete index")
        # Then ("Check that we can't delete index that was not created")
        index_name = 'id'
        assert_that(calling(drop_index).with_args(namespace, index_name),
                    raises(Exception, matching=has_string(f"Cannot remove index {index_name}: doesn't exist")),
                    "Not existing index was deleted")

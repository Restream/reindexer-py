from hamcrest import *

from qa_test.helpers.index import *
from qa_test.helpers.namespace import get_ns_description
from qa_test.test_data.constants import index_definition, updated_index_definition


class TestCrudIndexes:
    def test_initial_namespace_has_not_indexes(self, database, namespace):
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
        # db, namespace_name = namespace
        create_index(namespace, index_definition)
        # When ("Delete index")
        drop_index(namespace, 'id')
        # Then ("Check that index is deleted")
        ns_entry = get_ns_description(database, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", equal_to([]))),
                    "Index wasn't deleted")

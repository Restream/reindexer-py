from hamcrest import *

from tests.helpers.namespace import *


class TestCrudNamespace:
    def test_create_ns(self, database):
        # Given("Create namespace in empty database")
        namespace_name = 'test_ns'
        create_namespace(database, namespace_name)
        # When ("Get namespaces list in created database")
        namespace_list = get_namespace_list(database)
        # Then ("Check that database contains created namespace")
        assert_that(namespace_list, has_item(has_entry("name", equal_to(namespace_name))),
                    "Namespace wasn't created")
        drop_namespace(database, namespace_name)

    def test_delete_ns(self, database):
        # Given("Create namespace")
        namespace_name = 'test_ns'
        create_namespace(database, namespace_name)
        # When ("Delete namespace")
        drop_namespace(database, namespace_name)
        # Then ("Check that namespace was deleted")
        namespace_list = get_namespace_list(database)
        assert_that(namespace_list, not_(has_item(has_entry("name", equal_to(namespace_name)))),
                    "Namespace wasn't deleted")

    def test_cannot_delete_ns_not_created(self, database):
        # Given ("Create empty database")
        # Then ("Check that we cannot delete namespace that does not exist")
        namespace_name = 'test_ns'
        assert_that(calling(drop_namespace).with_args(database, namespace_name), raises(Exception, matching=has_string(
            f"Namespace '{namespace_name}' does not exist")))



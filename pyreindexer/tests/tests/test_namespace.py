from hamcrest import *

from pyreindexer.exceptions import ApiError


class TestCrudNamespace:

    def test_create_ns(self, db):
        # Given("Create namespace in empty database")
        namespace_name = 'test_ns1'
        db.namespace.open(namespace_name)
        # When ("Get namespaces list in created database")
        namespace_list = db.namespace.enumerate()
        # Then ("Check that database contains created namespace")
        assert_that(namespace_list, has_item(has_entries(name=namespace_name)),
                    "Namespace wasn't created")
        db.namespace.drop(namespace_name)

    def test_delete_ns(self, db):
        # Given("Create namespace in empty database")
        namespace_name = 'test_ns2'
        db.namespace.open(namespace_name)
        # When ("Delete namespace")
        db.namespace.drop(namespace_name)
        # Then ("Check that namespace was deleted")
        namespace_list = db.namespace.enumerate()
        assert_that(namespace_list, not_(has_item(has_entries(name=namespace_name))),
                    "Namespace wasn't deleted")

    def test_cannot_delete_ns_not_created(self, db):
        # Given ("Created empty database")
        # Then ("Check that we cannot delete namespace that does not exist")
        namespace_name = 'test_ns'
        assert_that(calling(db.namespace.drop).with_args(namespace_name),
                    raises(ApiError, pattern=f"Namespace '{namespace_name}' does not exist"))

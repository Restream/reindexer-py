from datetime import timedelta

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

    def test_drop_ns(self, db):
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


class TestNamespaceTimeouts:
    def test_namespace_timeouts(self, db):
        # When ("Create namespace with big timeout")
        ns_name = "test_ns_timeout"
        db.namespace.open(ns_name, timeout=timedelta(seconds=1))
        # Then ("Check that database contains created namespace")
        namespace_list = db.namespace.enumerate(timeout=timedelta(milliseconds=1000))
        assert_that(namespace_list, has_item(has_entries(name=ns_name)), "Namespace wasn't created")
        # When ("Delete namespace with big timeout")
        db.namespace.drop(ns_name, timeout=timedelta(milliseconds=1000))
        # Then ("Check that namespace was deleted")
        namespace_list = db.namespace.enumerate()
        assert_that(namespace_list, not_(has_item(has_entries(name=ns_name))), "Namespace wasn't deleted")

import json
from datetime import timedelta

from hamcrest import *

from pyreindexer.exceptions import ApiError
from tests.helpers.base_helper import create_items, get_ns_description, get_ns_items
from tests.test_data.constants import index_definition


class TestCrudNamespace:

    def test_create_ns(self, db):
        # Given("Create namespace in empty database")
        namespace_name = "test_ns_create"
        db.namespace.open(namespace_name, timeout=timedelta(seconds=1))
        # When ("Get namespaces list in created database")
        namespace_list = db.namespace.enumerate(timeout=timedelta(milliseconds=1000))
        # Then ("Check that database contains created namespace")
        assert_that(namespace_list, has_item(has_entries(name=namespace_name)),
                    "Namespace wasn't created")
        db.namespace.drop(namespace_name, timeout=timedelta(milliseconds=1000))

    def test_rename_ns(self, db):
        # Given("Create namespace in empty database")
        old_ns_name = "test_ns_for_rename"
        db.namespace.open(old_ns_name, timeout=timedelta(seconds=1))
        # When ("Get namespaces list in created database")
        new_ns_name = "test_ns_renamed"
        db.namespace.rename(old_ns_name, new_ns_name, timeout=timedelta(milliseconds=1000))
        namespace_list = db.namespace.enumerate(timeout=timedelta(milliseconds=1000))
        # Then ("Check that database contains renamed namespace")
        assert_that(namespace_list, has_item(has_entries(name=new_ns_name)))
        assert_that(namespace_list, not_(has_item(has_entries(name=old_ns_name))))
        db.namespace.drop(new_ns_name, timeout=timedelta(milliseconds=1000))

    def test_drop_ns(self, db):
        # Given("Create namespace in empty database")
        namespace_name = "test_ns_drop"
        db.namespace.open(namespace_name)
        # When ("Delete namespace")
        db.namespace.drop(namespace_name)
        # Then ("Check that namespace was deleted")
        namespace_list = db.namespace.enumerate()
        assert_that(namespace_list, not_(has_item(has_entries(name=namespace_name))),
                    "Namespace wasn't deleted")

    def test_truncate_ns(self, db):
        # Given("Create namespace with index and items")
        ns_name = "test_ns_truncate"
        db.namespace.open(ns_name)
        db.index.create(ns_name, index_definition, timeout=timedelta(milliseconds=1000))
        create_items(db, ns_name, [{"id": 0, "field": 0}, {"id": 1, "field": 2}])
        # When ("Truncate namespace")
        db.namespace.truncate(ns_name)
        # Then ("Check namespace is empty")
        ns_items = get_ns_items(db, ns_name)
        assert_that(ns_items, empty())

    def test_cannot_delete_ns_not_created(self, db):
        # Given ("Created empty database")
        # Then ("Check that we cannot delete namespace that does not exist")
        namespace_name = "test_ns_not_created"
        assert_that(calling(db.namespace.drop).with_args(namespace_name),
                    raises(ApiError, pattern=f"Namespace '{namespace_name}' does not exist"))


class TestSchema:

    def test_set_schema(self, db):
        # Given("Create namespace in empty database")
        namespace_name = "test_ns_schema"
        db.namespace.open(namespace_name, timeout=timedelta(seconds=1))
        # Given("Set namespace schema")
        schema = {"required": ["id"], "additionalProperties": False, "type": "object",
                  "properties": {"id": {"type": "integer"},
                                 "v1": {"type": "string"},
                                 "v2": {"type": "number"}}}
        db.schema.set(namespace_name, schema, timeout=timedelta(seconds=1))
        schema["x-protobuf-ns-number"] = 0
        # When ("Check that schema was set")
        ns_entry = get_ns_description(db, namespace_name)
        assert_that(ns_entry, has_length(1))
        assert_that(json.loads(ns_entry[0]["schema"]), equal_to(schema))

        # Given("Set another namespace schema")
        schema = {"required": ["id", "v2"], "additionalProperties": True, "type": "object",
                  "properties": {"id": {"type": "integer"},
                                 "v1": {"type": "string"},
                                 "v2": {"type": "boolean"}},
                  "x-protobuf-ns-number": 0}
        db.schema.set(namespace_name, schema, timeout=timedelta(seconds=1))
        # When ("Check that schema was set")
        ns_entry = get_ns_description(db, namespace_name)
        assert_that(ns_entry, has_item(has_entries(schema=json.dumps(schema))))

        db.namespace.drop(namespace_name, timeout=timedelta(milliseconds=1000))

from datetime import timedelta

import pytest
from hamcrest import *

from tests.helpers.base_helper import get_ns_items
from tests.test_data.constants import item_definition


class TestCrudItems:
    def test_initial_namespace_has_no_items(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Get namespace information")
        select_result = get_ns_items(db, namespace)
        # Then ("Check that list of items in namespace is empty")
        assert_that(select_result, empty(), "Item list is not empty")

    def test_create_item_insert(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Insert item into namespace")
        db.item.insert(namespace, item_definition)
        # Then ("Check that item is added")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, has_length(1), "Item wasn't created")
        assert_that(select_result, has_item(item_definition), "Item wasn't created")

    @pytest.mark.parametrize("value", [-1, -2.33])
    def test_create_item_insert_negative(self, db, namespace, index, value):
        # Given("Create namespace with index")
        # When ("Insert item into namespace")
        item_empty = {"id": -1, "field": value, "empty_field": None}
        db.item.insert(namespace, item_empty)
        # Then ("Check that item is added")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, has_length(1), "Item wasn't created")
        assert_that(select_result, has_item(item_empty), "Item wasn't created")

    def test_create_item_insert_with_precepts(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Insert items into namespace")
        number_items = 5
        for _ in range(number_items):
            db.item.insert(namespace, {"id": 100, "field": "value"}, ["id=serial()"])
        # Then ("Check that item is added")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, has_length(number_items), "Items wasn't created")
        for i in range(number_items):
            assert_that(select_result[i], equal_to({'id': i + 1, "field": "value"}), "Items wasn't created")

    def test_create_item_upsert(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Upsert item into namespace")
        db.item.upsert(namespace, item_definition)
        # Then ("Check that item is added")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, has_length(1), "Item wasn't created")
        assert_that(select_result, has_item(item_definition), "Item wasn't created")

    def test_update_item_upsert(self, db, namespace, index, item):
        # Given("Create namespace with item")
        # When ("Upsert item")
        item_definition_updated = {'id': 100, 'val': "new_value"}
        db.item.upsert(namespace, item_definition_updated)
        # Then ("Check that item is updated")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, has_length(1), "Item wasn't updated")
        assert_that(select_result, has_item(item_definition_updated), "Item wasn't updated")

    def test_update_item_update(self, db, namespace, index, item):
        # Given("Create namespace with item")
        # When ("Update item")
        item_definition_updated = {'id': 100, 'val': "new_value"}
        db.item.update(namespace, item_definition_updated)
        # Then ("Check that item is updated")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, has_length(1), "Item wasn't updated")
        assert_that(select_result, has_item(item_definition_updated), "Item wasn't updated")

    def test_delete_item(self, db, namespace, index, item):
        # Given("Create namespace with item")
        # When ("Delete item")
        db.item.delete(namespace, item_definition)
        # Then ("Check that item is deleted")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, empty(), "Item wasn't deleted")

    def test_item_timeouts(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Insert item into namespace with big timeout")
        db.item.insert(namespace, item_definition, timeout=timedelta(milliseconds=1000))
        # Then ("Check that item is added")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, has_length(1), "Item wasn't created")
        assert_that(select_result, has_item(item_definition), "Item wasn't created")
        # When ("Update item with big timeout")
        item_definition_updated = {'id': 100, 'val': "new_value"}
        db.item.update(namespace, item_definition_updated, timeout=timedelta(milliseconds=1000))
        # Then ("Check that item is updated")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, has_length(1), "Item wasn't updated")
        assert_that(select_result, has_item(item_definition_updated), "Item wasn't updated")
        # When ("Delete item with big timeout")
        db.item.delete(namespace, item_definition_updated, timeout=timedelta(milliseconds=1000))
        # Then ("Check that item is deleted")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, empty(), "Item wasn't deleted")

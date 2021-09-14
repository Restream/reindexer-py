from hamcrest import *

from tests.helpers.index import create_index
from tests.helpers.items import *
from tests.test_data.constants import item_definition


class TestCrudItems:
    def test_initial_namespace_has_no_items(self, namespace, index):
        # Given("Create namespace with index")
        db, namespace_name = namespace
        # When ("Get namespace information")
        select_result = list(db.select(f'SELECT * FROM {namespace_name}'))
        # Then ("Check that list of items in namespace is empty")
        assert_that(select_result, has_length(0), "Item list is not empty")
        assert_that(select_result, equal_to([]), "Item list is not empty")

    def test_create_item_insert(self, namespace, index):
        # Given("Create namespace with index")
        db, namespace_name = namespace
        # When ("Insert item into namespace")
        insert_item(namespace, item_definition)
        # Then ("Check that item is added")
        select_result = list(db.select(f'SELECT * FROM {namespace_name}'))
        assert_that(select_result, has_length(1),
                    "Item wasn't created")
        assert_that(select_result, has_item(item_definition),
                    "Item wasn't created"
                    )
        delete_item(namespace, item_definition)

    def test_create_item_insert_with_precepts(self, namespace, index):
        # Given("Create namespace with index")
        db, namespace_name = namespace
        # When ("Insert items into namespace")
        number_items = 5
        for _ in range(number_items):
            db.item_insert(namespace_name, {"id": 100, "field": "value"}, ["id=serial()"])
        # Then ("Check that item is added")
        select_result = list(db.select(f'SELECT * FROM {namespace_name}'))
        assert_that(select_result, has_length(number_items),
                    "Items wasn't created")
        for i in range(number_items):
            assert_that(select_result[i], equal_to({'id': i+1, "field": "value"}),
                    "Items wasn't created")
        for i in range(number_items):
            db.item_delete(namespace_name, {'id': i})

    def test_create_item_upsert(self, namespace, index):
        # Given("Create namespace with index")
        db, namespace_name = namespace
        # When ("Upsert item into namespace")
        upsert_item(namespace, item_definition)
        # Then ("Check that item is added")
        select_result = list(db.select(f'SELECT * FROM {namespace_name}'))
        assert_that(select_result, has_length(1),
                    "Item wasn't created")
        assert_that(select_result, has_item(item_definition),
                    "Item wasn't created")
        delete_item(namespace, item_definition)

    def test_update_item_upsert(self, namespace, index, item):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        # When ("Upsert item")
        item_definition_updated = {'id': 100, 'val': "new_value"}
        upsert_item(namespace, item_definition_updated)
        # Then ("Check that item is updated")
        select_result = list(db.select(f'SELECT * FROM {namespace_name}'))
        assert_that(select_result, has_length(1),
                    "Item wasn't updated")
        assert_that(select_result, has_item(item_definition_updated),
                    "Item wasn't updated")

    def test_update_item_update(self, namespace, index, item):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        # When ("Update item")
        item_definition_updated = {'id': 100, 'val': "new_value"}
        update_item(namespace, item_definition_updated)
        # Then ("Check that item is updated")
        select_result = list(db.select(f'SELECT * FROM {namespace_name}'))
        assert_that(select_result, has_length(1), "Item wasn't updated")
        assert_that(select_result, has_item(item_definition_updated), "Item wasn't updated")

    def test_delete_item(self, namespace, index):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        insert_item(namespace, item_definition)
        # When ("Delete item")
        delete_item(namespace, item_definition)
        # Then ("Check that item is deleted")
        select_result = list(db.select(f'SELECT * FROM {namespace_name}'))
        assert_that(select_result, has_length(0), "Item wasn't deleted")
        assert_that(select_result, equal_to([]), "Item wasn't deleted")

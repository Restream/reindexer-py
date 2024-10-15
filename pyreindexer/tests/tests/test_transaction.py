from hamcrest import *

from tests.helpers.items import *
from tests.helpers.transaction import *
from tests.test_data.constants import item_definition


class TestCrudTransaction:
    def test_initial_namespace_has_no_items(self, namespace, index):
        # Given("Create namespace with index")
        db, namespace_name = namespace
        # When ("Get namespace information")
        select_result = list(db.select(f'SELECT * FROM {namespace_name}'))
        # Then ("Check that list of items in namespace is empty")
        assert_that(select_result, has_length(0), "Transaction: item list is not empty")
        assert_that(select_result, equal_to([]), "Transaction: item list is not empty")

    def test_commit_after_rollback(self, namespace):
        # Given("Create namespace")
        db, namespace_name = namespace
        # When ("Start new transaction")
        transaction = db.new_transaction(namespace_name)
        # Then ("Rollback transaction")
        transaction.rollback()
        # Then ("Commit transaction")
        assert_that(calling(commit_transaction).with_args(transaction),
                    raises(Exception, matching=has_string("Transaction is over")))

    def test_rollback_after_commit(self, namespace):
        # Given("Create namespace")
        db, namespace_name = namespace
        # When ("Start new transaction")
        transaction = db.new_transaction(namespace_name)
        # Then ("Commit transaction")
        transaction.commit()
        # Then ("Rollback transaction")
        assert_that(calling(rollback_transaction).with_args(transaction),
                    raises(Exception, matching=has_string("Transaction is over")))

    def test_insert_after_rollback(self, namespace, index):
        # Given("Create namespace with index")
        db, namespace_name = namespace
        # When ("Start new transaction")
        transaction = db.new_transaction(namespace_name)
        # Then ("Rollback transaction")
        transaction.rollback()
        # Then ("Insert transaction")
        assert_that(calling(insert_transaction).with_args(transaction, item_definition),
                    raises(Exception, matching=has_string("Transaction is over")))

    def test_update_after_rollback(self, namespace, index):
        # Given("Create namespace with index")
        db, namespace_name = namespace
        # When ("Start new transaction")
        transaction = db.new_transaction(namespace_name)
        # Then ("Rollback transaction")
        transaction.rollback()
        # Then ("Update transaction")
        assert_that(calling(update_transaction).with_args(transaction, item_definition),
                    raises(Exception, matching=has_string("Transaction is over")))

    def test_upsert_after_rollback(self, namespace, index):
        # Given("Create namespace with index")
        db, namespace_name = namespace
        # When ("Start new transaction")
        transaction = db.new_transaction(namespace_name)
        # Then ("Rollback transaction")
        transaction.rollback()
        # Then ("Upsert transaction")
        assert_that(calling(upsert_transaction).with_args(transaction, item_definition),
                    raises(Exception, matching=has_string("Transaction is over")))

    def test_delete_after_rollback(self, namespace, index):
        # Given("Create namespace with index")
        db, namespace_name = namespace
        # When ("Start new transaction")
        transaction = db.new_transaction(namespace_name)
        # Then ("Rollback transaction")
        transaction.rollback()
        # Then ("Delete transaction")
        assert_that(calling(delete_transaction).with_args(transaction, item_definition),
                    raises(Exception, matching=has_string("Transaction is over")))

    def test_create_item_insert(self, namespace, index):
        # Given("Create namespace with index")
        db, namespace_name = namespace
        # When ("Insert item into namespace")
        insert_item_transaction(namespace, item_definition)
        # Then ("Check that item is added")
        select_result = list(db.select(f'SELECT * FROM {namespace_name}'))
        assert_that(select_result, has_length(1), "Transaction: item wasn't created")
        assert_that(select_result, has_item(item_definition), "Transaction: item wasn't created")
        delete_item(namespace, item_definition)

    def test_create_item_insert_with_precepts(self, namespace, index):
        # Given("Create namespace with index")
        db, namespace_name = namespace
        # When ("Insert items into namespace")
        transaction = db.new_transaction(namespace_name)
        number_items = 5
        for _ in range(number_items):
            transaction.insert({"id": 100, "field": "value"}, ["id=serial()"])
        transaction.commit()
        # Then ("Check that item is added")
        select_result = list(db.select(f'SELECT * FROM {namespace_name}'))
        assert_that(select_result, has_length(number_items), "Transaction: items wasn't created")
        for i in range(number_items):
            assert_that(select_result[i], equal_to({'id': i + 1, "field": "value"}),
                        "Transaction: items wasn't created")
        for i in range(number_items):
            db.item_delete(namespace_name, {'id': i})

    def test_create_item_upsert(self, namespace, index):
        # Given("Create namespace with index")
        db, namespace_name = namespace
        # When ("Upsert item into namespace")
        upsert_item_transaction(namespace, item_definition)
        # Then ("Check that item is added")
        select_result = list(db.select(f'SELECT * FROM {namespace_name}'))
        assert_that(select_result, has_length(1), "Transaction: item wasn't created")
        assert_that(select_result, has_item(item_definition), "Transaction: item wasn't created")
        delete_item(namespace, item_definition)

    def test_update_item_upsert(self, namespace, index, item):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        # When ("Upsert item")
        item_definition_updated = {'id': 100, 'val': "new_value"}
        upsert_item_transaction(namespace, item_definition_updated)
        # Then ("Check that item is updated")
        select_result = list(db.select(f'SELECT * FROM {namespace_name}'))
        assert_that(select_result, has_length(1), "Transaction: item wasn't updated")
        assert_that(select_result, has_item(item_definition_updated), "Transaction: item wasn't updated")

    def test_update_item_update(self, namespace, index, item):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        # When ("Update item")
        item_definition_updated = {'id': 100, 'val': "new_value"}
        update_item_transaction(namespace, item_definition_updated)
        # Then ("Check that item is updated")
        select_result = list(db.select(f'SELECT * FROM {namespace_name}'))
        assert_that(select_result, has_length(1), "Transaction: item wasn't updated")
        assert_that(select_result, has_item(item_definition_updated), "Transaction: item wasn't updated")

    def test_delete_item(self, namespace, index, item):
        # Given("Create namespace with item")
        db, namespace_name = namespace
        # When ("Delete item")
        delete_item_transaction(namespace, item)
        # Then ("Check that item is deleted")
        select_result = list(db.select(f'SELECT * FROM {namespace_name}'))
        assert_that(select_result, has_length(0), "Transaction: item wasn't deleted")
        assert_that(select_result, equal_to([]), "Transaction: item wasn't deleted")

    def test_rollback_transaction(self, namespace, index):
        # Given("Create namespace with index")
        db, namespace_name = namespace
        # When ("Insert items into namespace")
        transaction = db.new_transaction(namespace_name)
        number_items = 5
        for _ in range(number_items):
            transaction.insert({"id": 100, "field": "value"}, ["id=serial()"])
        # Then ("Rollback transaction")
        transaction.rollback()
        # When ("Get namespace information")
        select_result = list(db.select(f'SELECT * FROM {namespace_name}'))
        # Then ("Check that list of items in namespace is empty")
        assert_that(select_result, has_length(0), "Transaction: item list is not empty")
        assert_that(select_result, equal_to([]), "Transaction: item list is not empty")

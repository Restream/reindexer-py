import time
from datetime import timedelta

import pytest
from hamcrest import *

from pyreindexer.exceptions import TransactionError
from pyreindexer.query import CondType
from tests.helpers.base_helper import get_ns_items, get_ns_vect_items,random_vector
from tests.helpers.matchers import close_to_dict
from tests.helpers.transaction import *
from tests.test_data.constants import item_definition, vector_index_bf, vector_index_hnsw, vector_index_ivf


class TestCrudTransaction:
    def test_negative_commit_after_rollback(self, db, namespace):
        # Given("Create namespace")
        # When ("Start new transaction")
        transaction = db.tx.begin(namespace)
        # Then ("Rollback transaction")
        transaction.rollback()
        # Then ("Commit transaction")
        assert_that(calling(transaction.commit).with_args(),
                    raises(TransactionError, matching=has_string("Transaction is over")))

    def test_negative_rollback_after_commit(self, db, namespace):
        # Given("Create namespace")
        # When ("Start new transaction")
        transaction = db.tx.begin(namespace)
        # Then ("Commit transaction")
        transaction.commit()
        # Then ("Rollback transaction")
        assert_that(calling(transaction.rollback).with_args(),
                    raises(TransactionError, matching=has_string("Transaction is over")))

    def test_negative_insert_after_rollback(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Start new transaction")
        transaction = db.tx.begin(namespace)
        # Then ("Rollback transaction")
        transaction.rollback()
        # Then ("Insert transaction")
        assert_that(calling(transaction.insert_item).with_args(item_definition),
                    raises(TransactionError, matching=has_string("Transaction is over")))

    def test_negative_update_after_rollback(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Start new transaction")
        transaction = db.tx.begin(namespace)
        # Then ("Rollback transaction")
        transaction.rollback()
        # Then ("Update transaction")
        assert_that(calling(transaction.update_item).with_args(item_definition),
                    raises(TransactionError, matching=has_string("Transaction is over")))

    def test_negative_upsert_after_rollback(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Start new transaction")
        transaction = db.tx.begin(namespace)
        # Then ("Rollback transaction")
        transaction.rollback()
        # Then ("Upsert transaction")
        assert_that(calling(transaction.upsert_item).with_args(item_definition),
                    raises(TransactionError, matching=has_string("Transaction is over")))

    def test_negative_delete_after_rollback(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Start new transaction")
        transaction = db.tx.begin(namespace)
        # Then ("Rollback transaction")
        transaction.rollback()
        # Then ("Delete transaction")
        assert_that(calling(transaction.delete_item).with_args(item_definition),
                    raises(TransactionError, matching=has_string("Transaction is over")))

    def test_negative_insert_after_commit(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Start new transaction")
        transaction = db.tx.begin(namespace)
        # Then ("Commit transaction")
        transaction.commit()
        # Then ("Insert transaction")
        assert_that(calling(transaction.insert_item).with_args(item_definition),
                    raises(TransactionError, matching=has_string("Transaction is over")))

    def test_negative_update_after_commit(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Start new transaction")
        transaction = db.tx.begin(namespace)
        # Then ("Commit transaction")
        transaction.commit()
        # Then ("Update transaction")
        assert_that(calling(transaction.update_item).with_args(item_definition),
                    raises(TransactionError, matching=has_string("Transaction is over")))

    def test_negative_upsert_after_commit(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Start new transaction")
        transaction = db.tx.begin(namespace)
        # Then ("Commit transaction")
        transaction.commit()
        # Then ("Upsert transaction")
        assert_that(calling(transaction.upsert_item).with_args(item_definition),
                    raises(TransactionError, matching=has_string("Transaction is over")))

    def test_negative_delete_after_commit(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Start new transaction")
        transaction = db.tx.begin(namespace)
        # Then ("Commit transaction")
        transaction.commit()
        # Then ("Delete transaction")
        assert_that(calling(transaction.delete_item).with_args(item_definition),
                    raises(TransactionError, matching=has_string("Transaction is over")))

    def test_create_item_insert(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Insert item into namespace")
        transaction = db.tx.begin(namespace, timeout=timedelta(milliseconds=1000))
        transaction.insert_item(item_definition)
        transaction.commit(timeout=timedelta(milliseconds=1000))
        # Then ("Check that item is added")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, has_length(1), "Transaction: item wasn't created")
        assert_that(select_result, has_item(item_definition), "Transaction: item wasn't created")

    @pytest.mark.parametrize("vector_index", [vector_index_bf, vector_index_hnsw, vector_index_ivf])
    def test_insert_item_with_vector_index(self, db, namespace, index, vector_index):
        # Given("Create namespace")
        # When ("Add index")
        db.index.create(namespace, vector_index)
        # When ("Insert item into namespace")
        transaction = db.tx.begin(namespace)
        dimension = vector_index["config"]["dimension"]
        item = {"id": 0, "vec": random_vector(dimension)}
        transaction.insert_item(item)
        transaction.commit()
        # Then ("Check that item is added")
        select_result = get_ns_vect_items(db, namespace)
        assert_that(select_result, has_length(1), "Item wasn't created")
        assert_that(select_result[0], close_to_dict(item))

    def test_create_item_insert_with_precepts(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Insert items into namespace")
        transaction = db.tx.begin(namespace)
        number_items = 5
        for i in range(number_items):
            transaction.insert_item({'id': 100, 'field': f'value{100 + i}'}, ['id=serial()'])
        count = transaction.commit_with_count()
        assert_that(count, equal_to(number_items), "Transaction: items wasn't created")
        # Then ("Check that item is added")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, has_length(number_items), "Transaction: items wasn't created")
        for i in range(number_items):
            assert_that(select_result[i],
                        equal_to({'id': i + 1, 'field': f'value{100 + i}'}),
                        "Transaction: items wasn't created")

    def test_create_item_upsert(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Upsert item into namespace")
        upsert_item_transaction(db, namespace, item_definition)
        # Then ("Check that item is added")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, has_length(1), "Transaction: item wasn't created")
        assert_that(select_result, has_item(item_definition), "Transaction: item wasn't created")

    def test_update_item_upsert(self, db, namespace, index, item):
        # Given("Create namespace with item")
        # When ("Upsert item")
        item_definition_updated = {'id': 100, 'val': "new_value"}
        upsert_item_transaction(db, namespace, item_definition_updated)
        # Then ("Check that item is updated")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, has_length(1), "Transaction: item wasn't updated")
        assert_that(select_result, has_item(item_definition_updated), "Transaction: item wasn't updated")

    def test_update_item_update(self, db, namespace, index, item):
        # Given("Create namespace with item")
        # When ("Update item")
        item_definition_updated = {'id': 100, 'val': "new_value"}
        update_item_transaction(db, namespace, item_definition_updated)
        # Then ("Check that item is updated")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, has_length(1), "Transaction: item wasn't updated")
        assert_that(select_result, has_item(item_definition_updated), "Transaction: item wasn't updated")

    def test_delete_item(self, db, namespace, index, item):
        # Given("Create namespace with item")
        # When ("Delete item")
        delete_item_transaction(db, namespace, item)
        # Then ("Check that item is deleted")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, empty(), "Transaction: item wasn't deleted")

    def test_rollback_transaction(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Insert items into namespace")
        transaction = db.tx.begin(namespace)
        number_items = 5
        for i in range(number_items):
            transaction.insert_item({"id": i, "field": "value"})
        # Then ("Rollback transaction")
        transaction.rollback(timeout=timedelta(milliseconds=1000))
        # When ("Get namespace information")
        select_result = get_ns_items(db, namespace)
        # Then ("Check that list of items in namespace is empty")
        assert_that(select_result, empty(), "Transaction: item list is not empty")

    def test_commit_tx_timeout_small(self, db, namespace, index):
        """ Check that timeout is only for tx begin/commit methods, and not for the whole tx """
        # Given("Create namespace with index")
        # When ("Begin tx with small timeout, insert item")
        transaction = db.tx.begin(namespace, timeout=timedelta(milliseconds=20))
        time.sleep(0.1)
        transaction.insert_item(item_definition)
        # When ("Commit tx with small timeout")
        transaction.commit(timeout=timedelta(milliseconds=20))
        # Then ("Check that item was added")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, has_length(1), "Transaction: item wasn't created")
        assert_that(select_result, has_item(item_definition), "Transaction: item wasn't created")

    def test_transaction_query_delete(self, db, namespace, index, items):
        # Given("Create namespace with items")
        # When ("Delete items with transaction")
        transaction = db.tx.begin(namespace)
        query = db.query.new(namespace)
        query.where('id', CondType.CondGe, 0)
        transaction.delete_query(query)
        transaction.commit(timeout=timedelta(milliseconds=1000))
        # Then ("Check that items is deleted")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, empty(), "Transaction: item wasn't deleted")

    def test_transaction_query_update(self, db, namespace, index, item):
        # Given("Create namespace with item")
        # When ("Update item")
        item_definition_updated = {'id': 100, 'val': "new_value"}
        transaction = db.tx.begin(namespace)
        query = db.query.new(namespace)
        query.where('id', CondType.CondEq, 100).set('val', ['new_value'])
        transaction.update_query(query)
        transaction.commit(timeout=timedelta(milliseconds=1000))
        # Then ("Check that item is updated")
        select_result = get_ns_items(db, namespace)
        assert_that(select_result, has_length(1), "Transaction: item wasn't updated")
        assert_that(select_result, has_item(item_definition_updated), "Transaction: item wasn't updated")

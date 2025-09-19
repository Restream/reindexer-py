import random

from datetime import timedelta
from typing import Final, List

from pyreindexer import RxConnector
from pyreindexer.index_search_params import IndexSearchParamHnsw
from pyreindexer.exceptions import ApiError
from pyreindexer.query import CondType


def create_index_example(db, namespace):
    index_definition = {
        'name': 'id',
        'json_paths': ['id'],
        'field_type': 'int',
        'index_type': 'hash',
        'is_pk': True,
        'is_array': False,
        'is_dense': False,
        'is_sparse': False,
        'is_no_column': False,
        'collate_mode': 'none',
        'sort_order_letters': '',
        'expire_after': 0,
        'config': {},
    }

    try:
        db.index_add(namespace, index_definition)
    except ApiError:
        db.index_drop(namespace, 'id', timedelta(milliseconds = 1000))
        db.index_add(namespace, index_definition)


def update_index_example(db, namespace):
    index_definition_modified = {
        'name': 'id',
        'json_paths': ['id'],
        'field_type': 'int64',
        'index_type': 'hash',
        'is_pk': True,
        'is_array': False,
        'is_dense': True,
        'is_sparse': False,
        'is_no_column': False,
        'collate_mode': 'none',
        'sort_order_letters': '',
        'expire_after': 0,
        'config': {},
    }
    db.index_update(namespace, index_definition_modified)


def create_items_example(db, namespace):
    items_count = 10

    for i in range(0, items_count):
        item = {'id': 1, 'name': 'item_' + str(i % 2), 'value': 'check'}
        db.item_upsert(namespace, item, ["id=serial()"])


def select_item_query_example(db, namespace):
    item_name_for_lookup = 'item_0'

    return db.exec_sql(f"SELECT * FROM {namespace} WHERE name='{item_name_for_lookup}'", timedelta(milliseconds = 1000))

def select_all_item_query_example(db, namespace):
    return db.exec_sql(f'SELECT * FROM {namespace}', timedelta(milliseconds = 1000))

def print_all_records_from_namespace(db, namespace, message):
    selected_items_tr = select_all_item_query_example(db, namespace)

    res_count = selected_items_tr.count()
    print(message, res_count)

    for item in selected_items_tr:
        print(f'item: {item}')

def transaction_example(db, namespace, items_in_base):
    # start transaction
    transaction = db.new_transaction(namespace)

    items_count = len(items_in_base)

    # delete first few items
    for i in range(int(items_count / 2)):
        transaction.delete(items_in_base[i])

    # update last one item, overwrite field 'value'
    item = items_in_base[items_count - 1]
    item['value'] = 'transaction was here'
    transaction.update(item)

    # stop transaction and commit changes to namespace
    count = transaction.commit_with_count(timedelta(milliseconds = 1000))
    print(f'Transaction updated count: {count}')

    print_all_records_from_namespace(db, namespace, 'Transaction results count: ')

def query_example(db, namespace):
    # query all items
    any_items = (db.new_query(namespace)
                 .where('value', CondType.CondAny)
                 .sort('id')
                 .execute())
    print(f'Query results count (Any): {any_items.count()}')
    for item in any_items:
        print(f'item: {item}')

    # query some items
    selected_items = (db.new_query(namespace)
                      .where('value', CondType.CondEq, 'check')
                      .sort('id')
                      .limit(4)
                      .execute(timedelta(milliseconds = 1000)))
    print(f'Query results count (limited): {selected_items.count()}')
    for item in selected_items:
        print(f'item: {item}')

    # delete some items
    del_count = (db.new_query(namespace)
                 .where('name', CondType.CondEq, 'item_1')
                 .delete(timedelta(milliseconds = 1000)))
    print(f'Deleted count: {del_count}')

    # query all actual items
    any_items = (db.new_query(namespace)
                 .where('value', CondType.CondAny)
                 .must_execute())
    print(f'Query results count (Any after delete): {any_items.count()}')
    for item in any_items:
        print(f'item: {item}')

def modify_query_transaction(db, namespace):
    # start transaction
    transaction = db.new_transaction(namespace)

    # create an update query and set it for the transaction
    query_upd = db.new_query(namespace).where("id", CondType.CondLe, 5).set("name", ["update_with_query_tx"])
    transaction.update_query(query_upd)

    # create a delete query and set it for the transaction
    query_del = db.new_query(namespace).where("id", CondType.CondGe, 6)
    transaction.delete_query(query_del)

    # stop transaction and commit changes to namespace
    transaction.commit(timedelta(milliseconds = 1000))

    print_all_records_from_namespace(db, namespace, 'Transaction with Query results count: ')

def random_vector(dimension: int) -> List[float]:
    return [random.uniform(-10.0, 10.0) for _ in range(dimension)]

def float_vector_hnsw_example(db):
    namespace = 'knn_hnsw'
    db.namespace_open(namespace)

    # create index
    fv_index_name = 'hnsw_idx'
    dimension: Final[int] = 4
    index_definitions = [{'name': 'id',
                          'json_paths': ['id'],
                          'field_type': 'int',
                          'index_type': 'hash',
                          'is_pk': True,
                          'is_array': False,
                          'is_dense': False,
                          'is_sparse': False,
                          'is_no_column': False,
                          'collate_mode': 'none',
                          'sort_order_letters': '',
                          'expire_after': 0,
                          'config': {}},
                         {"name": fv_index_name,
                          "json_paths": [fv_index_name],
                          "field_type": "float_vector",
                          "index_type": "hnsw",
                          "config": {
                              "dimension": dimension,
                              "metric": "inner_product",
                              "start_size": 100,
                              "m": 16,
                              "ef_construction": 200,
                              "multithreading": 1}}]
    for index in index_definitions:
        db.index_add(namespace, index)

    # generate items
    transaction = db.new_transaction(namespace)
    for i in range(100):
        transaction.insert({"id": 0, fv_index_name: random_vector(dimension)}, ["id=serial()"])
    transaction.commit(timedelta(seconds = 3))

    # do query
    param = IndexSearchParamHnsw(k=20, ef=30)
    query_result = (db.new_query(namespace)
                        .where_knn(fv_index_name, random_vector(dimension), param)
                        .select_fields("vectors()")
                        .with_rank()
                        .sort(index="rank()", desc=True)
                        .must_execute(timedelta(seconds = 1)))

    # result
    print("HNSW where_knn: ", query_result.count())
    for item in query_result:
        print('item vec: ', item, end='\n')

    # drop index
    db.index_drop(namespace, fv_index_name, timedelta(milliseconds = 300))

def float_vector_brute_force_sql_example(db):
    namespace = 'knn_bf'
    db.namespace_open(namespace)

    # create index
    fv_index_name = 'bf_idx'
    dimension: Final[int] = 4
    index_definitions = [{'name': 'id',
                          'json_paths': ['id'],
                          'field_type': 'int',
                          'index_type': 'hash',
                          'is_pk': True,
                          'is_array': False,
                          'is_dense': False,
                          'is_sparse': False,
                          'is_no_column': False,
                          'collate_mode': 'none',
                          'sort_order_letters': '',
                          'expire_after': 0,
                          'config': {}},
                         {"name": fv_index_name,
                          "json_paths": [fv_index_name],
                          "field_type": "float_vector",
                          "index_type": "vec_bf",
                          "config": {
                              "dimension": 3,
                              "metric": "inner_product",
                              "start_size": 10000}}]
    for index in index_definitions:
        db.index_add(namespace, index)

    # update index
    index_definition_modified = {"name": fv_index_name,
                                 "json_paths": [fv_index_name],
                                 "field_type": "float_vector",
                                 "index_type": "vec_bf",
                                 "config": {
                                     "dimension": dimension,
                                     "metric": "l2",
                                     "start_size": 1000}}
    db.index_update(namespace, index_definition_modified)

    # generate items
    transaction = db.new_transaction(namespace)
    for i in range(100):
        transaction.insert({"id": i, fv_index_name: random_vector(dimension)})
    transaction.commit(timedelta(seconds = 3))

    # execute SQL query SELECT KNN
    value = random_vector(dimension)
    k: Final[int] = 27
    query = f'SELECT *, vectors() FROM {namespace} WHERE KNN({fv_index_name}, {value}, k={k})'
    query_result = db.exec_sql(query, timedelta(seconds = 1))
    print("Select where KNN: ", query_result.count())
    for item in query_result:
        print('item vec: ', item, end='\n')

    # drop index
    db.index_drop(namespace, fv_index_name, timedelta(milliseconds = 300))


def rx_example():

    db = RxConnector(f'builtin:///tmp/pyrx', max_replication_updates_size = 10 * 1024 * 1024)
    #db = RxConnector('cproto://127.0.0.1:6534/pyrx', enable_compression = True, fetch_amount = 500)

    namespace = 'test_table'
    db.namespace_open(namespace)

    create_index_example(db, namespace)
    update_index_example(db, namespace)

    create_items_example(db, namespace)
    print_all_records_from_namespace(db, namespace, 'All items: ')

    selected_items = select_item_query_example(db, namespace)

    res_count = selected_items.count()
    print(f'Results count: {res_count}')

    # disposable QueryResults iterator
    items_copy = []
    for item in selected_items:
        items_copy.append(item)
        print(f'item: {item}')

    # won't be iterated again
    for item in selected_items:
        print(f'item: {item}')

    transaction_example(db, namespace, items_copy)

    query_example(db, namespace)

    modify_query_transaction(db, namespace)

    float_vector_hnsw_example(db)
    float_vector_brute_force_sql_example(db)

    db.close()


if __name__ == "__main__":
    rx_example()

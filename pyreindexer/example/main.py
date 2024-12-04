from pyreindexer import RxConnector
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
        'collate_mode': 'none',
        'sort_order_letters': '',
        'expire_after': 0,
        'config': {},
    }

    try:
        db.index_add(namespace, index_definition)
    except (Exception,):
        db.index_drop(namespace, 'id')
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
        'collate_mode': 'none',
        'sort_order_letters': '',
        'expire_after': 0,
        'config': {},
    }
    db.index_update(namespace, index_definition_modified)


def create_items_example(db, namespace):
    items_count = 10

    for i in range(0, items_count):
        item = {'id': i + 1, 'name': 'item_' + str(i % 2), 'value': 'check'}
        db.item_upsert(namespace, item)


def select_item_query_example(db, namespace):
    item_name_for_lookup = 'item_0'

    return (db.with_timeout(1000)
                .select("SELECT * FROM " + namespace + " WHERE name='" + item_name_for_lookup + "'"))


def transaction_example(db, namespace, items_in_base):
    transaction = db.new_transaction(namespace)

    items_count = len(items_in_base)

    # delete first few items
    for i in range(int(items_count/2)):
        transaction.delete(items_in_base[i])

    # update last one item, overwrite field 'value'
    item = items_in_base[items_count - 1]
    item['value'] = 'transaction was here'
    transaction.update(item)

    # stop transaction and commit changes to namespace
    transaction.commit()

    # print records from namespace
    selected_items_tr = select_item_query_example(db, namespace)

    res_count = selected_items_tr.count()
    print('Transaction results count: ', res_count)

    # disposable QueryResults iterator
    for item in selected_items_tr:
        print('Item: ', item)


def query_example(db, namespace):
    any_items = (db.new_query(namespace)
                 .where('value', CondType.CondAny)
                 .sort('id')
                 .execute())
    print(f'Query results count (Any): {any_items.count()}')
    for item in any_items:
        print('Item: ', item)

    selected_items = (db.new_query(namespace)
                      .where('value', CondType.CondEq, 'check')
                      .sort('id')
                      .limit(4)
                      .execute())
    print(f'Query results count (limited): {selected_items.count()}')
    for item in selected_items:
        print('Item: ', item)

    del_count = (db.new_query(namespace)
                 .where('name', CondType.CondEq, 'item_1')
                 .delete())
    print(f'Deleted count: {del_count}')

    any_items = (db.new_query(namespace)
                 .where('value', CondType.CondAny)
                 .must_execute())
    print(f'Query results count (Any after delete): {any_items.count()}')
    for item in any_items:
        print('Item: ', item)


def rx_example():
    db = RxConnector('builtin:///tmp/pyrx', max_replication_updates_size = 10 * 1024 * 1024)
#    db = RxConnector('cproto://127.0.0.1:6534/pyrx', enable_compression = True, fetch_amount = 500)

    namespace = 'test_table'

    db.namespace_open(namespace)

    create_index_example(db, namespace)
    update_index_example(db, namespace)

    create_items_example(db, namespace)

    selected_items = select_item_query_example(db, namespace)

    res_count = selected_items.count()
    print('Results count: ', res_count)

    # disposable QueryResults iterator
    items_copy = []
    for item in selected_items:
        items_copy.append(item)
        print('Item: ', item)

    # won't be iterated again
    for item in selected_items:
        print('Item: ', item)

    transaction_example(db, namespace, items_copy)

    query_example(db, namespace)

    db.close()


if __name__ == "__main__":
    rx_example()

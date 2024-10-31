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

    return db.select("SELECT * FROM " + namespace + " WHERE name='" + item_name_for_lookup + "'")


def transaction_example(db, namespace, items_in_base):
    transaction = db.new_transaction(namespace)

    items_count = len(items_in_base)

    # delete first few items
    for i in range(int(items_count/2)):
        transaction.delete(items_in_base[i])

    # update last one item, overwrite field 'value'
    item = items_in_base[items_count - 1]
    item['value'] = 'the transaction was here'
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
    (db.new_query(namespace)
        .open_bracket()
        .where_between_fields('fld1', CondType.CondEq, 'fld2')
        .close_bracket()
        .where('fld2', CondType.CondLe, [42])
        .limit(10)
        .debug(1)
        .request_total())

    query = db.new_query(namespace).offset(1).cached_total()
    (query.where('fld1', CondType.CondSet, ['s','t','o','p'])
        .op_not()
        .where('fld2', CondType.CondSet, [3.14])
        .where_query(db.new_query(namespace), CondType.CondSet, ['to','check'])
        .explain()
        .fetch_count(10))
    query.expression('fld1', 'array_remove(integer_array, [5,6,7,8]) || [1,2,3]').drop('fld2')

    db.new_query(namespace).sort_stfield_distance('fldGeom1', 'fldGeom2', False)


def rx_example():
    db = RxConnector('builtin:///tmp/pyrx')
#    db = RxConnector('cproto://127.0.0.1:6534/pyrx')

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

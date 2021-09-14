from tests.helpers.log_helper import log_operation


def insert_item(namespace, item_def):
    """
    Insert item to namespace
    """
    db, namespace_name = namespace
    log_operation.info(f"Insert item: {item_def} to namespace {namespace_name}")
    db.item_insert(namespace_name, item_def)


def upsert_item(namespace, item_def):
    """
    Insert or update item to namespace
    """
    db, namespace_name = namespace
    log_operation.info(f"Upsert item: {item_def} to namespace {namespace_name}")
    db.item_upsert(namespace_name, item_def)


def update_item(namespace, item_def):
    """
    Update item to namespace
    """
    db, namespace_name = namespace
    log_operation.info(f"Update item: {item_def} to namespace {namespace_name}")
    db.item_upsert(namespace_name, item_def)


def delete_item(namespace, item_def):
    """
    Delete item from namespace
    """
    db, namespace_name = namespace
    log_operation.info(f"Delete item: {item_def} from namespace {namespace_name}")
    db.item_delete(namespace_name, item_def)

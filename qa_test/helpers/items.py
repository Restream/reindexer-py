def insert_item(namespace, item_def):
    """
    Insert item on namespace
    """
    db, namespace_name = namespace
    db.item_insert(namespace_name, item_def)


def upsert_item(namespace, item_def):
    """
    Insert or update item on namespace
    """
    db, namespace_name = namespace
    db.item_upsert(namespace_name, item_def)


def update_item(namespace, item_def):
    """
    Update item on namespace
    """
    db, namespace_name = namespace
    db.item_upsert(namespace_name, item_def)


def delete_item(namespace, item_def):
    """
    Delete item from namespace
    """
    db, namespace_name = namespace
    db.item_delete(namespace_name, item_def)
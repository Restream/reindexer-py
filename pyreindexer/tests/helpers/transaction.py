def insert_item_transaction(db, namespace, item_definition):
    """
    Insert an item into namespace using transaction
    """
    transaction = db.tx.begin(namespace)
    transaction.item_insert(item_definition)
    transaction.commit()


def upsert_item_transaction(db, namespace, item_definition):
    """
    Upsert or update an item into namespace using transaction
    """
    transaction = db.tx.begin(namespace)
    transaction.item_upsert(item_definition)
    transaction.commit()


def update_item_transaction(db, namespace, item_definition):
    """
    Update an item in namespace using transaction
    """
    transaction = db.tx.begin(namespace)
    transaction.item_update(item_definition)
    transaction.commit()


def delete_item_transaction(db, namespace, item_definition):
    """
    Delete item from namespace using transaction
    """
    transaction = db.tx.begin(namespace)
    transaction.item_delete(item_definition)
    transaction.commit()

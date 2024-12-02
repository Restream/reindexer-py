def insert_item_transaction(namespace, item_definition):
    """
    Insert an item into namespace using transaction
    """
    db, namespace_name = namespace
    transaction = db.new_transaction(namespace_name)
    transaction.insert(item_definition)
    transaction.commit()


def upsert_item_transaction(namespace, item_definition):
    """
    Insert or update an item into namespace using transaction
    """
    db, namespace_name = namespace
    transaction = db.new_transaction(namespace_name)
    transaction.upsert(item_definition)
    transaction.commit()


def update_item_transaction(namespace, item_definition):
    """
    Update an item in namespace using transaction
    """
    db, namespace_name = namespace
    transaction = db.new_transaction(namespace_name)
    transaction.update(item_definition)
    transaction.commit()


def delete_item_transaction(namespace, item_definition):
    """
    Delete item from namespace using transaction
    """
    db, namespace_name = namespace
    transaction = db.new_transaction(namespace_name)
    transaction.delete(item_definition)
    transaction.commit()


def commit_transaction(transaction):
    """
    Wrap a method call as a function (Commit)
    """
    transaction.commit()


def rollback_transaction(transaction):
    """
    Wrap a method call as a function (Rollback)
    """
    transaction.rollback()


def insert_transaction(transaction, item_def):
    """
    Wrap a method call as a function (Insert)
    """
    transaction.insert(item_def)


def update_transaction(transaction, item_def):
    """
    Wrap a method call as a function (Update)
    """
    transaction.update(item_def)


def upsert_transaction(transaction, item_def):
    """
    Wrap a method call as a function (Upsert)
    """
    transaction.upsert(item_def)


def delete_transaction(transaction, item_def):
    """
    Wrap a method call as a function (Delete)
    """
    transaction.delete(item_def)

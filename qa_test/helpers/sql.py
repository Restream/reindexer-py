from qa_test.helpers.log_helper import log_operation


def select_query(namespace, query):
    db, namespace_name = namespace
    item_list = list(db.select(query))
    log_operation.info(f"Execute SQL SELECT query: {query}, got result: {item_list}")
    return item_list

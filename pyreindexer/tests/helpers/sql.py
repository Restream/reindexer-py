from tests.helpers.log_helper import log_operation


def sql_query(namespace, query):
    db, namespace_name = namespace
    item_list = list(db.select(query))
    log_operation.info(f"Execute SQL query: {query}, got result: {item_list}")
    return item_list

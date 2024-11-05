from .log_helper import log_operation


def sql_query(namespace, query):
    db, namespace_name = namespace
    items_list = list(db.select(query))
    log_operation.info(f"Execute SQL query: {query}, got result: {items_list}")
    return items_list

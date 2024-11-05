import logging

from .log_helper import log_operation


def create_namespace(database, namespace_name):
    """
    Create a namespace
    """
    db, db_name = database
    log_operation.info(f"Create a namespace with name '{namespace_name}' on database '{db_name}'")
    try:
        db.namespace_open(namespace_name)
    except Exception as e:
        logging.error(e)


def drop_namespace(database, namespace_name):
    """
    Drop a namespace
    """
    db, db_name = database
    log_operation.info(f"Drop a namespace with name '{namespace_name}' on database '{db_name}'")
    db.namespace_drop(namespace_name)


def get_namespaces_list(database):
    """
    Get list of namespaces in database
    """
    log_operation.info("Get list of namespaces in database")
    db, db_name = database
    namespaces_list = db.namespaces_enum()
    return namespaces_list


def get_ns_description(database, namespace):
    """
    Get information about namespace in database
    """
    db, namespace_name = namespace
    namespace_list = get_namespaces_list(database)
    log_operation.info(f"Get information about namespace {namespace_name} in database")
    ns_entry = [ns for ns in namespace_list if ns["name"] == namespace_name]
    return ns_entry

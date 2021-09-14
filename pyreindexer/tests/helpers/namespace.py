import logging

from tests.helpers.log_helper import log_operation


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


def get_namespace_list(database):
    """
    Get list of namespaces in database
    """
    log_operation.info("Get list of namespaces in database")
    db, db_name = database
    namespace_list = db.namespaces_enum()
    return namespace_list


def get_ns_description(database, namespace):
    """
    Get information about namespace in database
    """
    db, namespace_name = namespace
    namespace_list = get_namespace_list(database)
    log_operation.info(f"Get information about namespace {namespace_name} in database")
    ns_entry = list(filter(lambda ns: ns['name'] == namespace_name, namespace_list))
    return ns_entry

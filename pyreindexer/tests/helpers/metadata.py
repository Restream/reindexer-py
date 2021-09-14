from tests.helpers.log_helper import log_operation


def put_metadata(namespace, key, value):
    db, namespace_name = namespace
    log_operation.info(f"Put metadata '{key}: {value}' to namespace '{namespace_name}'")
    db.meta_put(namespace_name, key, value)
    return key, value


def get_metadata_keys(namespace):
    db, namespace_name = namespace
    log_operation.info("Get list of metadata keys")
    meta_list = db.meta_enum(namespace_name)
    return meta_list


def get_metadata_by_key(namespace, key):
    db, namespace_name = namespace
    value = db.meta_get(namespace_name, key)
    log_operation.info(f"Get metadata value by key: '{key}: {value}'")
    return value

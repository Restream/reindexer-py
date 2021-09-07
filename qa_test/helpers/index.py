from hamcrest import *

from qa_test.helpers.log_helper import log_operation
from qa_test.helpers.namespace import get_ns_description
from qa_test.test_data.constants import index_definition, updated_index_definition, special_namespaces, item_definition


def create_index(namespace, index_def):
    """
    Create an index
    """
    log_operation.info(f"Create an index")
    db, namespace_name = namespace
    log_operation.info(f"on namespace '{namespace_name}', index={index_def}")
    db.index_add(namespace_name, index_def)


def update_index(namespace, index_def):
    """
    Update an index
    """
    db, namespace_name = namespace
    log_operation.info(f"on namespace '{namespace_name}', new index={index_def}")
    db.index_update(namespace_name, index_def)


def drop_index(namespace, index_name):
    """
    Drop index from namespace
    """
    log_operation.info(f"Drop index from namespace")
    db, namespace_name = namespace
    log_operation.info(f"on namespace '{namespace_name}', index name = '{index_name}'")
    db.index_drop(namespace_name, index_name)

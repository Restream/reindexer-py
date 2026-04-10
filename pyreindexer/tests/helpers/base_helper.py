import math
import random
import time
from typing import List

from tests.test_data.constants import index_definition


def create_items(db, ns, items: list):
    """ Create items
    """
    for item in items:
        db.item.insert(ns, item)


def get_ns_items(db, ns_name):
    """ Get all items via sql query
    """
    return list(db.query.sql(f"SELECT * FROM {ns_name}"))


def get_ns_vect_items(db, ns_name):
    """ Get all items via sql query
    """
    return list(db.query.sql(f"SELECT *, vectors() FROM {ns_name}"))


def get_ns_description(db, ns_name):
    """ Get information about namespace in database
    """
    namespaces_list = db.namespace.enumerate()
    ns_entry = [ns for ns in namespaces_list if ns["name"] == ns_name]
    return ns_entry


def prepare_ns_with_items(db, ns_name="new_ns", items_num=5) -> list:
    """ Create ns, index and items
    """
    db.namespace.open(ns_name)
    db.index.create(ns_name, index_definition)
    items = [{"id": i, "val": f"testval{i}"} for i in range(items_num)]
    for item in items:
        db.item.insert(ns_name, item)
    return items


def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def random_vector(dimension: int) -> List[float]:
    return [random.uniform(-10.0, 10.0) for _ in range(dimension)]


def await_vectors_quantization(db, ns, index):
    q = f"SELECT indexes FROM #memstats WHERE name = '{ns}'"
    time_start = time.time()
    while time.time() - time_start <= 30:
        r = list(db.query.sql(q))
        if r:
            found_index = [idx for idx in r[0]["indexes"] if idx["name"] == index["name"]]
            if found_index and found_index[0]["is_quantized"]:
                return
        time.sleep(0.1)
    raise TimeoutError("Too long index quantization")

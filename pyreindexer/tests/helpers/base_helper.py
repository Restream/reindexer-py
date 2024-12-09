import math


def get_ns_items(db, ns_name):
    """ Get all items via sql query
    """
    return list(db.query.sql(f"SELECT * FROM {ns_name}"))


def get_ns_description(db, ns_name):
    """ Get information about namespace in database
    """
    namespaces_list = db.namespace.enumerate()
    ns_entry = [ns for ns in namespaces_list if ns["name"] == ns_name]
    return ns_entry


def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

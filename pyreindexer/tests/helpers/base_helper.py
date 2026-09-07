import copy
import math
import random
import time
from collections import Counter
from typing import List

from tests.test_data.constants import COND_MAP, index_definition


def supplement_index(index: dict) -> None:
    if not index.get("json_paths"):
        index["json_paths"] = [index["name"]]
    if not index.get("index_type"):
        index["index_type"] = "hash"


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


def get_zero_value_for(field_type: str):
    if field_type == "string":
        return ""
    elif field_type == "bool":
        return False
    elif field_type == "uuid":
        return "00000000-0000-0000-0000-000000000000"
    elif field_type == "double":
        return 0.0
    elif field_type == "float_vector":
        return []
    else:
        return 0


def get_absent_value(field_type, is_sparse, is_array):
    if is_sparse:
        return None
    if is_array:
        return []
    return get_zero_value_for(field_type)


def is_empty(val):
    return val is None or val == []


def flatten_list(lst):
    result = []
    for element in lst:
        if isinstance(element, list):
            result.extend(flatten_list(element))
        else:
            result.append(element)
    return result


def try_convert(v1, v2):
    try:
        v1_conv = type(v2)(v1)
        return v1_conv, v2
    except (ValueError, TypeError):
        pass
    try:
        v2_conv = type(v1)(v2)
        return v1, v2_conv
    except (ValueError, TypeError):
        pass
    return v1, v2


def compare_by_cond(cond_f, field_1, field_2, item_1, item_2, default_val_1, default_val_2):
    value_1 = item_1.get(field_1, default_val_1)
    value_2 = item_2.get(field_2, default_val_2)

    if is_empty(value_1) and is_empty(value_2):
        return False

    is_array_1 = isinstance(value_1, list)
    is_array_2 = isinstance(value_2, list)
    if is_array_1 and is_array_2:
        array_1_values = flatten_list(value_1)
        array_2_values = flatten_list(value_2)
        return any(item in array_2_values for item in array_1_values)
    elif is_array_1:
        array_1_values = flatten_list(value_1)
        return value_2 in array_1_values
    elif is_array_2:
        array_2_values = flatten_list(value_2)
        return value_1 in array_2_values

    if cond_f != "eq" and (is_empty(value_1) or is_empty(value_2)):
        return False

    if not isinstance(value_1, type(value_2)):
        value_1, value_2 = try_convert(value_1, value_2)

    return cond_f(value_1, value_2)


def get_items_with_selected_fields(items: List[dict], select_filters: List[str], keep_joined=True) -> list:
    items_new_list = []
    for item in items:
        new_item = {}
        for k, v in item.items():
            if k in select_filters or (keep_joined and k.startswith("joined_")):
                new_item[k] = v
        items_new_list.append(new_item)
    return items_new_list


def _get_on_fields(on_field):
    if isinstance(on_field, str):
        on_field1 = on_field2 = on_field
    else:
        on_field1, on_field2 = on_field
    return on_field1, on_field2


def get_joined(items_1, join_type, items_2, on_field, second_namespace, select_filter_1=None, select_filter_2=None,
               cond="eq", is_not=False, is_sparse_1=False, is_sparse_2=False, is_array_1=False, is_array_2=False,
               field_type_1="int", field_type_2="int") -> list:
    cond_f = COND_MAP[cond.lower()]
    if items_1 and not isinstance(items_1[0], dict):
        items_1 = [i.to_dict() for i in items_1]
    if items_2 and not isinstance(items_2[0], dict):
        items_2 = [i.to_dict() for i in items_2]
    if select_filter_1:
        items_1 = get_items_with_selected_fields(items_1, select_filter_1)
    joined_ns_name = (f"joined_{second_namespace}" if isinstance(second_namespace, str)
                      else f"joined_{second_namespace.name}")

    default_val_1 = get_absent_value(field_type_1, is_sparse_1, is_array_1)
    default_val_2 = get_absent_value(field_type_2, is_sparse_2, is_array_2)

    on_field1, on_field2 = _get_on_fields(on_field)
    result_items = []
    for item1 in items_1:
        if is_not:
            item1[joined_ns_name] = [item2 for item2 in items_2 if not compare_by_cond(
                cond_f, on_field1, on_field2, item1, item2, default_val_1, default_val_2)]
        else:
            item1[joined_ns_name] = [item2 for item2 in items_2 if compare_by_cond(
                cond_f, on_field1, on_field2, item1, item2, default_val_1, default_val_2)]

        if select_filter_2:
            item1[joined_ns_name] = get_items_with_selected_fields(item1[joined_ns_name], select_filter_2)

        if item1[joined_ns_name]:
            result_items.append(item1)
        elif join_type.lower() == "left":
            del item1[joined_ns_name]
            result_items.append(item1)
    return result_items


def _evaluate_logical_operators(child_results: list) -> bool:
    """
      - AND1 OR AND2 AND3       → (AND1 OR AND2) AND AND3
      - NOT1 NOT2 OR            → NOT1 AND (NOT2 OR)
      - OR1 OR2 OR3             → ((OR1 OR OR2) OR OR3)
      - AND1 OR1 OR2            → ((AND1 OR OR1) OR OR2)
    """
    if not child_results:
        return True

    def is_child_success(r):
        return r["failed"] if r["op"] == "NOT" else not r["failed"]

    groups = [is_child_success(child_results[0])]
    for cr in child_results[1:]:
        if cr["op"] == "OR":
            groups[-1] = groups[-1] or is_child_success(cr)
        else:
            groups.append(is_child_success(cr))

    return all(groups)


def _get_on_conditions(spec):
    """ if spec doesn't contain 'on_conditions' - normalize 'on_field' and build 'on_conditions' """
    if "on_conditions" in spec:
        return spec["on_conditions"]
    on_left, on_right = _get_on_fields(spec.get("on_field"))
    cond_spec = {"on_left": on_left, "on_right": on_right}
    for key in ("is_sparse_left", "is_sparse_right", "is_array_left", "is_array_right",
                "field_type_left", "field_type_right"):
        if key in spec:
            cond_spec[key] = spec[key]
    return [cond_spec]


def _find_joined_by_on_conditions(item, items_to_join, on_conditions):
    """ find joined items, based on ON-conditions """
    matched_list = []

    for cond_num, cond_spec in enumerate(on_conditions):
        cond = cond_spec.get("cond", "eq").lower()
        cond_f = COND_MAP[cond]
        on_left = cond_spec["on_left"]
        on_right = cond_spec["on_right"]
        op = cond_spec.get("op", "and").lower()

        default_val_left = get_absent_value(
            cond_spec.get("field_type_left", "string"),
            cond_spec.get("is_sparse_left", False),
            cond_spec.get("is_array_left", False)
        )
        default_val_right = get_absent_value(
            cond_spec.get("field_type_right", "string"),
            cond_spec.get("is_sparse_right", False),
            cond_spec.get("is_array_right", False)
        )

        join_filtered = []
        for item2 in items_to_join:
            if compare_by_cond(cond_f, on_left, on_right, item, item2, default_val_left, default_val_right):
                join_filtered.append(item2)

        if cond_num == 0:
            if op == "and":
                matched_list = join_filtered
            elif op == "not":
                matched_list = [i for i in items_to_join if i not in join_filtered]
            else:
                raise ValueError("The first cond cannot be OR")
        else:
            if op == "and":
                matched_list = [i for i in matched_list if i in join_filtered]
            elif op == "or":
                matched_list.extend(i for i in join_filtered if i not in matched_list)
            else:  # not
                matched_list = [i for i in matched_list if i not in join_filtered]

    return matched_list


def _apply_specs_to_items(items: list, specs: list):
    if not items:
        return []
    if not specs:
        return items

    ns_counter = Counter()
    for spec in specs:
        ns_name = spec["joined_ns"].name if hasattr(spec["joined_ns"], "name") else spec["joined_ns"]
        ns_counter[ns_name] += 1
    repeated_ns = {ns for ns, count in ns_counter.items() if count > 1}

    result = []
    for item in items:
        ns_current_count = {}
        child_results = []

        for spec in specs:
            join_type = spec["join_type"].lower()
            op = spec.get("op", "AND").upper()

            items_to_join = spec["items"]
            if items_to_join and not isinstance(items_to_join[0], dict):
                items_to_join = [i.to_dict() for i in items_to_join]

            ns_name = spec["joined_ns"].name if hasattr(spec["joined_ns"], "name") else spec["joined_ns"]
            if ns_name in repeated_ns:
                ns_current_count[ns_name] = ns_current_count.get(ns_name, 0) + 1
                joined_ns_name = f"joined_{ns_current_count[ns_name]}_{ns_name}"
            else:
                joined_ns_name = f"joined_{ns_name}"

            on_conditions = _get_on_conditions(spec)
            joined = _find_joined_by_on_conditions(item, items_to_join, on_conditions)

            limit = spec.get("limit")
            children = spec.get("children", [])

            valid_joined = []
            if not joined:
                failed = (join_type == "inner")
            else:
                if limit is not None and limit > 0:
                    joined = joined[:limit]

                for j in joined:
                    j_copy = copy.deepcopy(j)
                    j_copy = _apply_children(j_copy, children)
                    if j_copy is not None:
                        valid_joined.append(j_copy)

                if not valid_joined:
                    failed = (join_type == "inner")
                elif limit == 0:
                    valid_joined = []
                    failed = False
                else:
                    failed = False

            child_results.append({
                "op": op,
                "join_type": join_type,
                "joined_ns_name": joined_ns_name,
                "valid_joined": valid_joined,
                "select_filter": spec.get("select_filter"),
                "failed": failed
            })

        if _evaluate_logical_operators(child_results):
            for cr in child_results:
                if cr["valid_joined"]:
                    if cr["select_filter"]:
                        item[cr["joined_ns_name"]] = get_items_with_selected_fields(
                            cr["valid_joined"], cr["select_filter"]
                        )
                    else:
                        item[cr["joined_ns_name"]] = cr["valid_joined"]
            result.append(item)

    return result


def _apply_children(item, children: list):
    if not children:
        return item
    result = _apply_specs_to_items([item], children)
    return result[0] if result else None


def get_nested_joined(items: list, join_specs) -> list:
    if not items:
        return []
    items = [i.to_dict() for i in items] if not isinstance(items[0], dict) else [copy.deepcopy(i) for i in items]

    if isinstance(join_specs, dict):
        join_specs = [join_specs]

    return _apply_specs_to_items(items, join_specs)


def sort_nested_joins(items):
    for item in items:
        for key, value in item.items():
            if key.startswith("joined_") and isinstance(value, list):
                value.sort(key=lambda x: x.get("id", 0))
                sort_nested_joins(value)

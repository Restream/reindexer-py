from hamcrest import *

from tests.helpers.base_helper import get_items_with_selected_fields, get_joined, get_nested_joined, sort_nested_joins
from tests.helpers.matchers import close_to_dict


def check_response_has_close_to_ns_items(res_items, ns_items, delta=0.01):
    assert_that(res_items, not_(empty()))
    for res_item in res_items:
        assert_that(ns_items, has_item(close_to_dict(res_item, delta)))


def check_response_has_only_close_to_items(res_items, items):
    assert_that(res_items, has_length(len(items)))
    used_ids = set()
    for res_item in res_items:
        assert_that(items, has_item(close_to_dict(res_item)))
        item_id = res_item["id"]
        assert item_id not in used_ids, f"Duplicate id {item_id} in response"
        used_ids.add(item_id)
    assert used_ids == {item["id"] for item in items}, "Mismatched IDs"


###--  JOIN  --###

def check_join(r, items_1, join_type, items_2, on_field, second_namespace, select_filter_1=None, select_filter_2=None,
               cond="eq", is_not=False, is_sparse_1=False, is_sparse_2=False, is_array_1=False, is_array_2=False,
               field_type_1="int", field_type_2="int"):
    expected_items = get_joined(items_1, join_type, items_2, on_field, second_namespace, select_filter_1,
                                select_filter_2, cond, is_not, is_sparse_1, is_sparse_2, is_array_1, is_array_2,
                                field_type_1, field_type_2)
    res_items = r["items"] if isinstance(r, dict) else r
    assert_that(res_items, contains_inanyorder(*expected_items))


def check_nested_join(res_items, items1, nested_join_spec, select_filter=None):
    expected_items = get_nested_joined(items1, nested_join_spec)
    if select_filter:
        expected_items = get_items_with_selected_fields(expected_items, select_filter)

    sort_nested_joins(res_items)
    sort_nested_joins(expected_items)
    assert_that(res_items, contains_inanyorder(*expected_items))

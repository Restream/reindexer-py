from hamcrest import *

from tests.helpers.matchers import close_to_dict


def check_response_has_close_to_ns_items(res_items, ns_items, delta=0.01):
    assert_that(res_items, not_(empty()))
    for res_item in res_items:
        assert_that(ns_items, has_item(close_to_dict(res_item, delta)))


def check_response_has_only_close_to_items(res_items, items):
    assert_that(res_items, has_length(len(items)))
    for item in res_items:
        assert_that(items, has_item(close_to_dict(item)))
        found_item = [i for i in items if i["id"] == item["id"]][0]
        items.remove(found_item)
    assert_that(items, empty())

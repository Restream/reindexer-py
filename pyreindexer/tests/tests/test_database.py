from hamcrest import *

from tests.test_data.constants import special_namespaces, special_namespaces_cluster


class TestCrudDb:
    def test_create_db(self, db):
        # When ("Get namespaces list in created database")
        namespaces_list = db.namespace.enumerate()
        # Then ("Check that database contains only special namespaces")
        if len(namespaces_list) == len(special_namespaces_cluster):
            expected_namespaces = special_namespaces_cluster  # v4
        else:
            expected_namespaces = special_namespaces  # v3
        assert_that(namespaces_list, has_length(len(expected_namespaces)),
                    "Database doesn't contain special namespaces")
        for namespace in expected_namespaces:
            assert_that(namespaces_list, has_item(has_entries(name=namespace["name"])),
                        "Database doesn't contain special namespaces")

import pyreindexer
from hamcrest import *

from tests.test_data.constants import special_namespaces, special_namespaces_cluster


class TestCrudDb:
    def test_create_db(self):
        # Given ("Create empty database")
        db_path = '/tmp/test_db'
        db = pyreindexer.RxConnector('builtin://' + db_path)
        # When ("Get namespaces list in created database")
        namespace_list = db.namespaces_enum()
        # Then ("Check that database contains only special namespaces")
        expect_namespaces = special_namespaces
        if len(namespace_list) == len(special_namespaces_cluster):
            expect_namespaces = special_namespaces_cluster
        for namespace in expect_namespaces:
            assert_that(namespace_list, has_item(has_entries("name", equal_to(namespace["name"]))),
                        "Database doesn't contain special namespaces")
        assert_that(namespace_list, has_length(equal_to(len(expect_namespaces))),
                    "Database doesn't contain special namespaces")

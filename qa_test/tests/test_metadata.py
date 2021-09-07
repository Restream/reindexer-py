from hamcrest import *


class TestCrudMetadata:
    def test_initial_namespace_has_not_metadata(self, namespace):
        # Given("Create namespace")
        db, namespace_name = namespace
        # When ("Get list of metadata keys")
        meta_list = db.meta_enum(namespace_name)
        # Then ("Check that list of metadata is empty")
        assert_that(meta_list, has_length(0), "Metadata is not empty")
        assert_that(meta_list, equal_to([]), "Metadata is not empty")

    def test_create_metadata(self, namespace):
        # Given("Create namespace")
        db, namespace_name = namespace
        # When ("Put metadata to namespace")
        key, value = 'key', 'value'
        db.meta_put(namespace_name, key, value)
        # Then ("Check that metadata was added")
        meta_list = db.meta_enum(namespace_name)
        assert_that(meta_list, has_length(1), "Metadata is not created")
        assert_that(meta_list, has_item(key), "Metadata is not created")

    def test_get_metdata_by_key(self, namespace, metadata):
        # Given ("Put metadata to namespace")
        db, namespace_name = namespace
        meta_key, meta_value = metadata
        # When ("Get metadata by key")
        meta_list = db.meta_get(namespace_name, meta_key)
        # Then ("Check that metadata was added")
        assert_that(meta_list, equal_to(meta_value), "Can't get meta value by key")

    def test_get_metadata_keys(self, namespace, metadata):
        # Given ("Put metadata to namespace")
        db, namespace_name = namespace
        meta_key, meta_value = metadata
        # When ("Get list of metadata keys")
        meta_list = db.meta_enum(namespace_name)
        # Then ("Check that metadata was added")
        assert_that(meta_list, has_item(meta_key), "Can't get list of meta keys")

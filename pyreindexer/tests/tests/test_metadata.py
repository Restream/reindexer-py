from hamcrest import *

from tests.helpers.metadata import *


class TestCrudMetadata:
    def test_initial_namespace_has_no_metadata(self, namespace):
        # Given("Create namespace")
        # When ("Get list of metadata keys")
        meta_list = get_metadata_keys(namespace)
        # Then ("Check that list of metadata is empty")
        assert_that(meta_list, has_length(0), "Metadata is not empty")
        assert_that(meta_list, equal_to([]), "Metadata is not empty")

    def test_create_metadata(self, namespace):
        # Given("Create namespace")
        # When ("Put metadata to namespace")
        key, value = 'key', 'value'
        put_metadata(namespace, key, value)
        # Then ("Check that metadata was added")
        meta_list = get_metadata_keys(namespace)
        assert_that(meta_list, has_length(1), "Metadata is not created")
        assert_that(meta_list, has_item(key), "Metadata is not created")

    def test_get_metadata_by_key(self, namespace, metadata):
        # Given ("Put metadata to namespace")
        meta_key, meta_value = metadata
        # When ("Get metadata by key")
        value = get_metadata_by_key(namespace, meta_key)
        # Then ("Check that metadata was added")
        assert_that(value, equal_to(meta_value), "Can't get meta value by key")

    def test_get_metadata_keys(self, namespace, metadata):
        # Given ("Put metadata to namespace")
        meta_key, meta_value = metadata
        # When ("Get list of metadata keys")
        meta_list = get_metadata_keys(namespace)
        # Then ("Check that metadata was added")
        assert_that(meta_list, has_item(meta_key), "Can't get list of meta keys")

    def test_update_metadata(self, namespace, metadata):
        # Given ("Put metadata to namespace")
        meta_key, meta_value = metadata
        # When ("Update metadata")
        new_meta_value = 'new_value'
        put_metadata(namespace, meta_key, new_meta_value)
        # Then ("Check that metadata was updated")
        updated_value = get_metadata_by_key(namespace, meta_key)
        assert_that(updated_value, equal_to(new_meta_value), "Can't update metadata")

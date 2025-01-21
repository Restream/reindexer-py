from datetime import timedelta

from hamcrest import *


class TestCrudMetadata:
    def test_initial_namespace_has_no_metadata(self, db, namespace):
        # Given("Create namespace")
        # When ("Get list of metadata keys")
        meta_list = db.meta.enumerate(namespace)
        # Then ("Check that list of metadata is empty")
        assert_that(meta_list, empty(), "Metadata is not empty")

    def test_create_metadata(self, db, namespace):
        # Given("Create namespace")
        # When ("Put metadata to namespace")
        key, value = 'key', 'value'
        db.meta.put(namespace, key, value)
        # Then ("Check that metadata was added")
        meta_list = db.meta.enumerate(namespace)
        assert_that(meta_list, has_length(1), "Metadata is not created")
        assert_that(meta_list, has_item(key), "Metadata is not created")

    def test_get_metadata_by_key(self, db, namespace, metadata):
        # Given ("Put metadata to namespace")
        meta_key, meta_value = metadata
        # When ("Get metadata by key")
        value = db.meta.get(namespace, meta_key)
        # Then ("Check that metadata was added")
        assert_that(value, equal_to(meta_value), "Can't get meta value by key")

    def test_get_metadata_keys(self, db, namespace, metadata):
        # Given ("Put metadata to namespace")
        meta_key, meta_value = metadata
        # When ("Get list of metadata keys")
        meta_list = db.meta.enumerate(namespace)
        # Then ("Check that metadata was added")
        assert_that(meta_list, has_item(meta_key), "Can't get list of meta keys")

    def test_update_metadata(self, db, namespace, metadata):
        # Given ("Put metadata to namespace")
        meta_key, meta_value = metadata
        # When ("Update metadata")
        new_meta_value = 'new_value'
        db.meta.put(namespace, meta_key, new_meta_value)
        # Then ("Check that metadata was updated")
        updated_value = db.meta.get(namespace, meta_key)
        assert_that(updated_value, equal_to(new_meta_value), "Can't update metadata")

    def test_delete_metadata(self, db, namespace, metadata):
        # Given ("Put metadata to namespace")
        meta_key, meta_value = metadata
        # When ("Delete metadata")
        db.meta.delete(namespace, meta_key)
        # Then ("Check that metadata was removed")
        read_value = db.meta.get(namespace, meta_key)
        assert_that(read_value, equal_to(''), "Can't delete metadata")
        # When ("Get list of metadata keys")
        meta_list = db.meta.enumerate(namespace)
        # Then ("Check that list of metadata is empty")
        assert_that(meta_list, empty(), "Metadata is not empty")

    def test_metadata_put_and_delete_timeouts(self, db, namespace):
        # Given("Create namespace")
        # When ("Put metadata to namespace with big timeout")
        key, value = "key", "value"
        db.meta.put(namespace, key, value, timeout=timedelta(milliseconds=1000))
        # Then ("Check that metadata was added")
        meta_list = db.meta.enumerate(namespace, timeout=timedelta(milliseconds=1000))
        assert_that(meta_list, has_length(1), "Metadata is not created")
        assert_that(meta_list, has_item(key), "Metadata is not created")
        # When ("Delete metadata with big timeout")
        db.meta.delete(namespace, key, timeout=timedelta(milliseconds=1000))
        # Then ("Check that metadata was removed")
        read_value = db.meta.get(namespace, key)
        assert_that(read_value, equal_to(''), "Can't delete metadata")
        # When ("Get list of metadata keys")
        meta_list = db.meta.enumerate(namespace)
        # Then ("Check that list of metadata is empty")
        assert_that(meta_list, empty(), "Metadata is not empty")

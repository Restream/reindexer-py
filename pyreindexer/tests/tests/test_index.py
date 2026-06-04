import copy
from datetime import timedelta
from typing import Final

import pytest
from hamcrest import *

from pyreindexer.exceptions import ApiError
from pyreindexer.index_definition import IndexDefinition
from tests.helpers.base_helper import get_ns_description
from tests.test_data.constants import (index_definition, updated_index_definition, vector_index_bf, vector_index_hnsw,
                                       vector_index_ivf)


class TestCrudIndexes:
    def test_initial_namespace_has_no_indexes(self, db, namespace):
        # Given("Create namespace")
        # When ("Get namespace information")
        ns_entry = get_ns_description(db, namespace)
        # Then ("Check that list of indexes in namespace is empty")
        assert_that(ns_entry, has_item(has_entry("indexes", empty())), "Index is not empty")

    def test_create_index(self, db, namespace):
        # Given("Create namespace")
        # When ("Add index")
        db.index.create(namespace, index_definition, timeout=timedelta(milliseconds=1000))
        # Then ("Check that index is added")
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(index_definition))),
                    "Index wasn't created")

    @pytest.mark.parametrize("vector_index", [vector_index_bf, vector_index_hnsw, vector_index_ivf])
    def test_create_vector_index(self, db, namespace, vector_index):
        # Given("Create namespace")
        # When ("Add index")
        db.index.create(namespace, vector_index)
        # Then ("Check that index is added")
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(vector_index))),
                    "Index wasn't created")

    def test_create_vector_index_quantized(self, db, namespace):
        # Given("Create namespace")
        # When ("Add index")
        vec_index = copy.deepcopy(vector_index_hnsw)
        vec_index["config"]["quantization_config"] = {"quantization_type": "scalar_quantization_8_bit",
                                                      "sample_size": 5, "quantization_threshold": 1}
        db.index.create(namespace, vec_index)
        # Then ("Check that index is added")
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(vec_index))))

    def test_update_vector_index_quantized(self, db, namespace):
        # Given("Create namespace")
        # When ("Add index")
        vec_index = copy.deepcopy(vector_index_hnsw)
        vec_index["config"]["quantization_config"] = {"quantization_type": "scalar_quantization_8_bit",
                                                      "sample_size": 5, "quantization_threshold": 1}
        db.index.create(namespace, vec_index)
        # When ("Update index")
        vec_index["config"]["quantization_config"] = {"quantization_type": "scalar_quantization_8_bit",
                                                      "sample_size": 10, "quantization_threshold": 2}
        db.index.update(namespace, vec_index)
        # Then ("Check that index is updated")
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(vec_index))))

    def test_update_vector_index_to_quantized(self, db, namespace):
        # Given("Create namespace")
        # When ("Add index")
        vec_index = copy.deepcopy(vector_index_hnsw)
        db.index.create(namespace, vec_index)
        # When ("Update index")
        vec_index["config"]["quantization_config"] = {"quantization_type": "scalar_quantization_8_bit",
                                                      "sample_size": 10, "quantization_threshold": 2}
        db.index.update(namespace, vec_index)
        # Then ("Check that index is updated")
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(vec_index))))

    def test_update_index(self, db, namespace, index):
        # Given("Create namespace with index")
        # When ("Update index")
        db.index.update(namespace, updated_index_definition)
        # Then ("Check that index is updated")
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(updated_index_definition))),
                    "Index wasn't updated")

    def test_delete_index(self, db, namespace):
        # Given("Create namespace with index")
        db.index.create(namespace, index_definition)
        # When ("Delete index")
        db.index.drop(namespace, 'id')
        # Then ("Check that index is deleted")
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", empty())), "Index wasn't deleted")

    def test_cannot_add_index_with_same_name(self, db, namespace):
        # Given("Create namespace")
        # When ("Add index")
        db.index.create(namespace, index_definition)
        # Then ("Check that we can't add index with the same name")
        assert_that(calling(db.index.create).with_args(namespace, updated_index_definition),
                    raises(ApiError, pattern="Index '.*' already exists with different settings"),
                    "Index with existing name was created")

    def test_cannot_update_not_existing_index_in_namespace(self, db, namespace):
        # Given ("Create namespace")
        # When ("Update index")
        # Then ("Check that we can't update index that was not created")
        assert_that(calling(db.index.update).with_args(namespace, index_definition),
                    raises(ApiError, pattern=f"Index 'id' not found in '{namespace}'"),
                    "Not existing index was updated")

    def test_cannot_delete_not_existing_index_in_namespace(self, db, namespace):
        # Given ("Create namespace")
        # When ("Delete index")
        # Then ("Check that we can't delete index that was not created")
        index_name = 'id'
        assert_that(calling(db.index.drop).with_args(namespace, index_name),
                    raises(ApiError, pattern=f"Cannot remove index '{index_name}': doesn't exist"),
                    "Not existing index was deleted")

    def test_index_update_timeout(self, db, namespace):
        # Given("Create index")
        db.index.create(namespace, index_definition, timeout=timedelta(milliseconds=1000))
        # When ("Update index with big timeout")
        db.index.update(namespace, updated_index_definition, timeout=timedelta(milliseconds=1000))
        # Then ("Check that index is updated")
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(updated_index_definition))),
                    "Index wasn't updated")

    def test_invalid_index_embedder_config(self, db, namespace, index):
        # Given ("Create float vector index")
        dimension: Final[int] = 5
        index = copy.deepcopy(vector_index_hnsw)
        index["config"]["dimension"] = dimension
        index["config"]["embedding"] = {
            "query_embedder": {"URL": "abc"}
        }
        err_msg = "Configuration 'embedding:query_embedder' contain field 'URL' with unexpected value: 'abc'"
        assert_that(calling(db.index.create).with_args(namespace, index), raises(ApiError, pattern=err_msg))


class TestIndexDefinition:

    def test_index_definition_init(self, db, namespace):
        # Given("Create namespace")
        # When ("Add index (init)")
        index_def = IndexDefinition(name="idx", field_type="int", index_type="hash", is_sparse=True)
        db.index.create(namespace, index_def)
        # Then ("Check that index is added")
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(index_def.to_dict()))))
        # Then ("Update index (dict-like)")
        index_def["index_type"] = "tree"
        index_def["is_dense"] = False
        db.index.update(namespace, index_def)
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(index_def.to_dict()))))
        # Then ("Update index (update method)")
        index_def.update({"collate_mode": "utf8", "is_no_column": True})
        db.index.update(namespace, index_def)
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(index_def.to_dict()))))

    def test_index_definition_fluent_interface(self, db, namespace):
        # Given("Create namespace")
        # When ("Add index (fluent interface)")
        index_def = (IndexDefinition().name("years").
                     json_paths(["year1", "year2"]).
                     field_type("int64").
                     index_type("-").
                     is_array())
        index_def.is_dense()
        db.index.create(namespace, index_def)
        # Then ("Check that index is added")
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(index_def.to_dict()))))
        # Then ("Update index (fluent interface)")
        index_def.index_type("hash").is_dense(False)
        db.index.update(namespace, index_def)
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(index_def.to_dict()))))

    def test_cant_create_index_without_required_fields(self, db, namespace):
        # Given("Create namespace")
        # When ("Create IndexDefinition object")
        index_def = IndexDefinition()
        # Then ("Check that we can't add index without name")
        assert_that(calling(db.index.create).with_args(namespace, index_def), raises(
            AttributeError, pattern="Index must contain field 'name'"
        ))
        index_def.name("index123")
        # Then ("Check that we can't add index without field_type")
        assert_that(calling(db.index.create).with_args(namespace, index_def), raises(
            AttributeError, pattern="Index must contain field 'field_type'"
        ))
        index_def.field_type("string")
        # Then ("Check that we can't add index without index_type")
        assert_that(calling(db.index.create).with_args(namespace, index_def), raises(
            AttributeError, pattern="Index must contain field 'index_type'"
        ))
        index_def.index_type("hash")
        # Then ("Now index can be created")
        db.index.create(namespace, index_def)
        ns_entry = get_ns_description(db, namespace)
        assert_that(ns_entry, has_item(has_entry("indexes", has_item(index_def.to_dict()))))

    def test_create_index_errors(self, db, namespace):
        # Given("Create namespace")
        # When ("Create IndexDefinition object")
        index_def = IndexDefinition(field_type="int", index_type="hash").name("idx")
        # Then ("Check that we can't use invalid field_type")
        assert_that(calling(index_def.field_type).with_args("random1"), raises(
            ValueError, pattern="field_type must be one of (.*), got 'random1'"
        ))
        # Then ("Check that we can't use invalid index_type")
        assert_that(calling(index_def.index_type).with_args("random2"), raises(
            ValueError, pattern="index_type must be one of (.*), got 'random2'"
        ))
        # Then ("Check that we can't add rtree_type to not geoindex")
        assert_that(calling(index_def.rtree_type).with_args("rstar"), raises(
            ValueError, pattern=r"rtree_type is only available for geoindex \(rtree, point\), not for \(hash, int\)"
        ))

    def test_index_attrs_errors(self, db, namespace):
        # Given("Create namespace")
        # When ("Create IndexDefinition object")
        index_def = IndexDefinition(name="idx", field_type="int", index_type="hash")
        # Then ("Check that we can't set invalid attribute")
        with pytest.raises(AttributeError, match="'IndexDefinition' object has no attribute 'rand1'"):
            index_def.rand1()
        # Then ("Check that we can't set invalid attribute (dict-like)")
        with pytest.raises(KeyError, match="Invalid index attribute 'rand3', must be one of (.*)"):
            index_def["rand3"] = "Hello"
        # Then ("Check that we can't get invalid attribute")
        with pytest.raises(KeyError, match="Invalid index attribute 'rand3', must be one of (.*)"):
            index_def["rand3"]

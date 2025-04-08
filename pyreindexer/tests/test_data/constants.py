index_definition = {
    "name": "id",
    "field_type": "int",
    "index_type": "hash",
    "is_pk": True,
    "is_array": False,
    "is_dense": False,
    "is_sparse": False,
    'is_no_column': False,
    "collate_mode": "none",
    "sort_order_letters": "",
    "config": {},
    "expire_after": 0,
    "json_paths": ["id"]
}

updated_index_definition = {
    "name": "id",
    "field_type": "int64",
    "index_type": "hash",
    "is_pk": True,
    "is_array": False,
    "is_dense": False,
    "is_sparse": False,
    'is_no_column': False,
    "collate_mode": "none",
    "sort_order_letters": "",
    "config": {},
    "expire_after": 0,
    "json_paths": ["id_new"]
}

composite_index_definition = {
    "name": "comp_idx",
    "field_type": "composite",
    "index_type": "hash",
    "is_pk": False,
    "is_array": False,
    "is_dense": False,
    "is_sparse": False,
    "json_paths": ["id", "val"]
}

vector_index_bf = {
    "name": "vec",
    "field_type": "float_vector",
    "index_type": "vec_bf",
    "is_pk": False,
    "is_array": False,
    "is_dense": False,
    "is_sparse": False,
    'is_no_column': False,
    "collate_mode": "none",
    "sort_order_letters": "",
    "expire_after": 0,
    "config": {"dimension": 4, "metric": "l2", "start_size": 1000},
    "json_paths": ["vec"]
}

vector_index_hnsw = {
    "name": "vec",
    "field_type": "float_vector",
    "index_type": "hnsw",
    "is_pk": False,
    "is_array": False,
    "is_dense": False,
    "is_sparse": False,
    'is_no_column': False,
    "collate_mode": "none",
    "sort_order_letters": "",
    "expire_after": 0,
    "config": {"dimension": 4, "metric": "inner_product", "start_size": 1000,
               "ef_construction": 20, "m": 4, "multithreading": 1},
    "json_paths": ["vec"]
}

vector_index_ivf = {
    "name": "vec",
    "field_type": "float_vector",
    "index_type": "ivf",
    "is_pk": False,
    "is_array": False,
    "is_dense": False,
    "is_sparse": False,
    'is_no_column': False,
    "collate_mode": "none",
    "sort_order_letters": "",
    "expire_after": 0,
    "config": {"dimension": 4, "metric": "cosine", "centroids_count": 10},
    "json_paths": ["vec"]
}

special_namespaces = [{"name": "#namespaces"},
                      {"name": "#memstats"},
                      {"name": "#perfstats"},
                      {"name": "#config"},
                      {"name": "#queriesperfstats"},
                      {"name": "#activitystats"},
                      {"name": "#clientsstats"}]

special_namespaces_cluster = [{"name": "#namespaces"},
                              {"name": "#memstats"},
                              {"name": "#perfstats"},
                              {"name": "#config"},
                              {"name": "#queriesperfstats"},
                              {"name": "#activitystats"},
                              {"name": "#clientsstats"},
                              {"name": "#replicationstats"}]

item_definition = {"id": 100, "val": "testval"}

AGGREGATE_FUNCTIONS_MATH = [(lambda x: max(x), "aggregate_max"),
                            (lambda x: min(x), "aggregate_min"),
                            (lambda x: sum(x), "aggregate_sum"),
                            (lambda x: sum(x) / len(x), "aggregate_avg")]

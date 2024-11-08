index_definition = {
    "name": "id",
    "field_type": "int",
    "index_type": "hash",
    "is_pk": True,
    "is_array": False,
    "is_dense": False,
    "is_sparse": False,
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

item_definition = {'id': 100, 'val': "testval"}

AGGREGATE_FUNCTIONS_MATH = [(lambda x: max(x), "aggregate_max"),
                            (lambda x: min(x), "aggregate_min"),
                            (lambda x: sum(x), "aggregate_sum"),
                            (lambda x: sum(x) / len(x), "aggregate_avg")]

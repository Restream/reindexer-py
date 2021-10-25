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
   "expire_after": 0,
   "config": {

   },
   "json_paths": [
      "id"
   ]
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
   "expire_after": 0,
   "config": {

   },
   "json_paths": [
      "id_new"
   ]
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


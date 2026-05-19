import json
from typing import Dict, List, Optional


class IndexDefinition:
    """ IndexDefinition allows to construct and manage indexes more efficiently using a fluent interface

    #### Examples:
        ### Create:
            - idx = IndexDefinition(name='test_index', field_type='string', index_type='hash', is_pk=True)
                OR
            - idx = IndexDefinition().name('test_index').field_type('string').index_type('hash').is_pk()
        ### Update:
            - idx['collate_mode'] = 'utf8'
                OR
            - idx.collate_mode('utf8')
        ### Get attribute value (only dict-like syntax):
            - idx_name = idx['name']

    #### Arguments:
        name (str): An index name
        json_paths (list[str]): JSON paths for mapping values to fields
        field_type (str): Field type. Possible values: `int`, `int64`, `double`, `string`, `bool`, 
            `uuid`, `point`, `composite`, `float_vector`
        index_type (str): Index type. Possible values: `hash`, `tree`, `text`, `-`, `rtree`, 
            `hnsw`, `vec_bf`, `ivf`
        is_pk (bool): True if field is a primary key
        is_array (bool): True if index is an array
        is_dense (bool): True if index is dense - reduce the index size,
            but for tree and hash indexes with low selectivity can seriously decrease update performance
        is_sparse (bool): True if index value may be absent
        is_no_column (bool): True to disable column subindex - reduces the index size, but may also reduce performance
        collate_mode (str): Collation order. Possible values: `none`, `ascii`, `utf8`, `numeric`, `custom`
        sort_order_letters (str): Custom sort order for `collate_mode='custom'`
        config (dict): Config for fulltext or float_vector engines
            [More about `fulltext`](https://github.com/Restream/reindexer/blob/master/fulltext.md)
            [More about `float_vector`](https://github.com/Restream/reindexer/blob/master/float_vector.md)
        expire_after (int): TTL in seconds
        rtree_type (str): RTree index type. Possible values: `rstar`, `linear`, `quadratic`, `greene`
    """

    _FIELD_TYPES = ("int", "int64", "double", "string", "bool", "uuid", "point", "composite", "float_vector")
    _INDEX_TYPES = ("hash", "tree", "text", "-", "rtree", "hnsw", "vec_bf", "ivf")
    _COLLATE_MODES = ("none", "ascii", "utf8", "numeric", "custom")
    _RTREE_TYPES = ("rstar", "linear", "quadratic", "greene")

    _ATTR_TYPES: Dict[str, type] = {
        "name": str,
        "json_paths": list,
        "field_type": str,
        "index_type": str,
        "is_pk": bool,
        "is_array": bool,
        "is_dense": bool,
        "is_sparse": bool,
        "is_no_column": bool,
        "collate_mode": str,
        "sort_order_letters": str,
        "config": dict,
        "expire_after": int,
        "rtree_type": str,
    }

    _INDEX_ATTRS = tuple(_ATTR_TYPES.keys())

    def __init__(
            self,
            name: str = "",
            json_paths: Optional[List[str]] = None,
            field_type: Optional[str] = None,
            index_type: Optional[str] = None,
            is_pk: bool = False,
            is_array: bool = False,
            is_dense: bool = False,
            is_sparse: bool = False,
            is_no_column: bool = False,
            collate_mode: Optional[str] = "none",
            sort_order_letters: str = "",
            config: Optional[Dict] = {},
            expire_after: int = 0,
            rtree_type: Optional[str] = None,
    ):
        if name is not None:
            self.name(name)
        if json_paths is not None:
            self.json_paths(json_paths)
        if field_type is not None:
            self.field_type(field_type)
        if index_type is not None:
            self.index_type(index_type)

        self.is_pk(is_pk)
        self.is_array(is_array)
        self.is_dense(is_dense)
        self.is_sparse(is_sparse)
        self.is_no_column(is_no_column)

        self.collate_mode(collate_mode)
        self.sort_order_letters(sort_order_letters)
        self.config(config)
        self.expire_after(expire_after)
        if rtree_type is not None:
            self.rtree_type(rtree_type)

    # ========== Validation ==========

    def _validate_type(self, value, attr: str):
        expected_type = self._ATTR_TYPES[attr]
        if not isinstance(value, expected_type):
            raise TypeError(f"{attr} must be of type {expected_type.__name__}, got {type(value).__name__}")

    @staticmethod
    def _validate_allowed_values(value: str, attr: str, allowed: tuple):
        if value not in allowed:
            raise ValueError(f"{attr} must be one of {allowed}, got '{value}'")

    def _validate_attr(self, attr: str):
        if attr not in self._INDEX_ATTRS:
            raise KeyError(f"Invalid index attribute '{attr}', must be one of {self._INDEX_ATTRS}")

    # ========== Fluent setters ==========

    def name(self, value: str) -> "IndexDefinition":
        self._validate_type(value, "name")
        self._name = value
        if not getattr(self, "_json_path", None):
            self.json_paths([self._name])
        return self

    def json_paths(self, value: List[str]) -> "IndexDefinition":
        if value is None:
            self._json_paths = self._name
            return self
        self._validate_type(value, "json_paths")
        if not all(isinstance(v, str) for v in value):
            raise TypeError("json_paths must be a list of strings")
        self._json_paths = value
        return self

    def field_type(self, value: str) -> "IndexDefinition":
        if not value:
            raise ValueError(f"field_type is not declared, must be one of: {self._FIELD_TYPES}")
        self._validate_type(value, "field_type")
        self._validate_allowed_values(value, "field_type", self._FIELD_TYPES)
        self._field_type = value
        return self

    def index_type(self, value: str) -> "IndexDefinition":
        if not value:
            raise ValueError(f"index_type is not declared, must be one of: {self._INDEX_TYPES}")
        self._validate_type(value, "index_type")
        self._validate_allowed_values(value, "index_type", self._INDEX_TYPES)
        self._index_type = value
        return self

    def is_pk(self, value: bool = True) -> "IndexDefinition":
        self._validate_type(value, "is_pk")
        self._is_pk = value
        return self

    def is_array(self, value: bool = True) -> "IndexDefinition":
        self._validate_type(value, "is_array")
        self._is_array = value
        return self

    def is_dense(self, value: bool = True) -> "IndexDefinition":
        self._validate_type(value, "is_dense")
        self._is_dense = value
        return self

    def is_sparse(self, value: bool = True) -> "IndexDefinition":
        self._validate_type(value, "is_sparse")
        self._is_sparse = value
        return self

    def is_no_column(self, value: bool = True) -> "IndexDefinition":
        self._validate_type(value, "is_no_column")
        self._is_no_column = value
        return self

    def collate_mode(self, value: str) -> "IndexDefinition":
        self._validate_type(value, "collate_mode")
        self._validate_allowed_values(value, "collate_mode", self._COLLATE_MODES)
        self._collate_mode = value
        return self

    def sort_order_letters(self, value: str) -> "IndexDefinition":
        self._validate_type(value, "sort_order_letters")
        self._sort_order_letters = value
        return self

    def config(self, value: Dict) -> "IndexDefinition":
        self._validate_type(value, "config")
        self._config = value
        return self

    def expire_after(self, value: int) -> "IndexDefinition":
        self._validate_type(value, "expire_after")
        self._expire_after = value
        return self

    def rtree_type(self, value: str) -> "IndexDefinition":
        self._validate_type(value, "rtree_type")
        self._validate_allowed_values(value, "rtree_type", self._RTREE_TYPES)
        if not (self._field_type == "point" and self._index_type == "rtree"):
            raise ValueError(f"rtree_type is only available for geoindex (rtree, point), "
                             f"not for ({self._index_type}, {self._field_type})")
        self._rtree_type = value
        return self

    # ========== Dict-like methods ==========

    def to_dict(self) -> dict:
        return {k[1:]: v for k, v in self.__dict__.items()}

    def __getitem__(self, attr: str):
        self._validate_attr(attr)
        return getattr(self, f"_{attr}")

    def __setitem__(self, attr: str, value):
        self._validate_attr(attr)
        setter_func = getattr(self, attr)
        setter_func(value)

    def __repr__(self) -> str:
        return json.dumps(self.to_dict())

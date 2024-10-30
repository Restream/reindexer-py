from __future__ import annotations
from typing import List, Union
from enum import Enum
from pyreindexer.point import Point

class CondType(Enum):
    CondAny = 0
    CondEq = 1
    CondLt = 2
    CondLe = 3
    CondGt = 4
    CondGe = 5
    CondRange = 6
    CondSet = 7
    CondAllSet = 8
    CondEmpty = 9
    CondLike = 10
    CondDWithin = 11

class StrictMode(Enum):
    NotSet = 0
    Empty = 1
    Names = 2
    Indexes = 3

class Query(object):
    """An object representing the context of a Reindexer query

    # Attributes:
        api (module): An API module for Reindexer calls
        query_wrapper_ptr (int): A memory pointer to Reindexer query object
        err_code (int): the API error code
        err_msg (string): the API error message

    """

    def __init__(self, api, query_wrapper_ptr: int):
        """Constructs a new Reindexer query object

        # Arguments:
            api (module): An API module for Reindexer calls
            query_wrapper_ptr (int): A memory pointer to Reindexer query object

        """

        self.api = api
        self.query_wrapper_ptr = query_wrapper_ptr
        self.err_code = 0
        self.err_msg = ""

    def __del__(self):
        """Free query memory

        """

        if self.query_wrapper_ptr > 0:
            self.api.delete_query(self.query_wrapper_ptr)

    def _raise_on_error(self):
        """Checks if there is an error code and raises with an error message

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        if self.err_code:
            raise Exception(self.err_msg)

    def where(self, index: str, condition: CondType, keys: List[Union[int,bool,float,str]] = ()) -> Query:
        """Add where condition to DB query with int args

        # Arguments:
            index (string): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            keys (list[Union[int,bool,float,str]]): Value of index to be compared with. For composite indexes keys must be list, with value of each subindex

        # Returns:
            (:obj:`Query`): Query object for further customizations

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.where(self.query_wrapper_ptr, index, condition.value, keys)
        self._raise_on_error()
        return self

    def where_query(self, sub_query: Query, condition: CondType, keys: List[Union[int,bool,float,str]] = ()) -> Query:
        """Add sub query where condition to DB query with int args

        # Arguments:
            sub_query (:obj:`Query`): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            keys (list[Union[int,bool,float,str]]): Value of index to be compared with. For composite indexes keys must be list, with value of each subindex

        # Returns:
            (:obj:`Query`): Query object for further customizations

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.where_query(self.query_wrapper_ptr, sub_query.query_wrapper_ptr, condition.value, keys)
        self._raise_on_error()
        return self

    def where_composite(self, index: str, condition: CondType, sub_query: Query) -> Query:
        """Add where condition to DB query with interface args for composite indexes

        # Arguments:
            index (string): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            sub_query (:obj:`Query`): Field name used in condition clause

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.where_composite(self.query_wrapper_ptr, index, condition.value, sub_query.query_wrapper_ptr)
        return self

    def where_uuid(self, index: str, condition: CondType, keys: List[str]) -> Query:
        """Add where condition to DB query with UUID as string args.
            This function applies binary encoding to the UUID value.
            'index' MUST be declared as uuid index in this case

        # Arguments:
            index (string): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            keys (list[string]): Value of index to be compared with. For composite indexes keys must be list, with value of each subindex

        # Returns:
            (:obj:`Query`): Query object for further customizations

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.where_uuid(self.query_wrapper_ptr, index, condition.value, keys)
        self._raise_on_error()
        return self

    def where_between_fields(self, first_field: str, condition: CondType, second_field: str) -> Query:
        """Add comparing two fields where condition to DB query

        # Arguments:
            first_field (string): First field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            second_field (string): Second field name used in condition clause

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.where_between_fields(self.query_wrapper_ptr, first_field, condition.value, second_field)
        return self

    def open_bracket(self) -> Query:
        """Open bracket for where condition to DB query

        # Returns:
            (:obj:`Query`): Query object for further customizations

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.open_bracket(self.query_wrapper_ptr)
        self._raise_on_error()
        return self

    def close_bracket(self) -> Query:
        """CloseBracket - Close bracket for where condition to DB query

        # Returns:
            (:obj:`Query`): Query object for further customizations

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.close_bracket(self.query_wrapper_ptr)
        self._raise_on_error()
        return self

    def match(self, index: str, keys: List[str]) -> Query:
        """Add string EQ-condition to DB query with string args

        # Arguments:
            index (string): Field name used in condition clause
            keys (list[string]): Value of index to be compared with. For composite indexes keys must be list, with value of each subindex

        # Returns:
            (:obj:`Query`): Query object for further customizations

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.where(self.query_wrapper_ptr, index, CondType.CondEq.value, keys)
        self._raise_on_error()
        return self

    def dwithin(self, index: str, point: Point, distance: float) -> Query:
        """Add DWithin condition to DB query

        # Arguments:
            index (string): Field name used in condition clause
            point (:obj:`Point`): Point object used in condition clause
            distance (float): Distance in meters between point

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.dwithin(self.query_wrapper_ptr, index, point.x, point.y, distance)
        return self

    def distinct(self, index: str) -> Query:
        """Performs distinct for a certain index.
            Return only items with uniq value of field

        # Arguments:
            index (string): Field name for distinct operation

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.aggregate_distinct(self.query_wrapper_ptr, index)
        return self

    def  aggregate_sum(self, index: str) -> Query:
        """Performs a summation of values for a specified index

        # Arguments:
            index (string): Field name for sum operation

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.aggregate_sum(self.query_wrapper_ptr, index)
        return self

    def aggregate_avg(self, index: str) -> Query:
        """Finds for the average at the specified index

        # Arguments:
            index (string): Field name for sum operation

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.aggregate_avg(self.query_wrapper_ptr, index)
        return self

    def aggregate_min(self, index: str) -> Query:
        """Finds for the minimum at the specified index

        # Arguments:
            index (string): Field name for sum operation

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.aggregate_min(self.query_wrapper_ptr, index)
        return self

    def aggregate_max(self, index: str) -> Query:
        """Finds for the maximum at the specified index

        # Arguments:
            index (string): Field name for sum operation

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.aggregate_max(self.query_wrapper_ptr, index)
        return self

################################################################ ToDo
#type AggregateFacetRequest struct {
#    query *Query
#}
#// fields should not be empty.
#func (q *Query) AggregateFacet(fields ...string) *AggregateFacetRequest {
#func (r *AggregateFacetRequest) Limit(limit int) *AggregateFacetRequest {
#func (r *AggregateFacetRequest) Offset(offset int) *AggregateFacetRequest {
#func (r *AggregateFacetRequest) Sort(field string, desc bool) *AggregateFacetRequest {
#func (q *Query) Sort(sortIndex string, desc bool, values ...interface{}) *Query {
#func (q *Query) SortStPointDistance(field string, p Point, desc bool) *Query {
################################################################

#func (q *Query) SortStFieldDistance(field1 string, field2 string, desc bool) *Query { // ToDo
#    def sort_stfield_distance(self, first_field: str, second_field: str, desc: bool) -> Query:
#        """Wrapper for geometry sorting by shortest distance between 2 geometry fields (ST_Distance)

#        # Arguments:
#            first_field (string): First field name used in condition
#            second_field (string): Second field name used in condition
#            desc (bool): Descending flag

#        # Returns:
#            (:obj:`Query`): Query object for further customizations

#        # Raises:
#            Exception: Raises with an error message of API return on non-zero error code

#        """

#        request : str = "ST_Distance("
#        request += first_field
#        request += ','
#        request += second_field
#        request += ')'

#        return self.sort(request, desc)
################################################################

    def op_and(self) -> Query:
        """Next condition will be added with AND.
            This is the default operation for WHERE statement. Do not have to be called explicitly in user's code.
            Used in DSL conversion

        # Returns:
            (:obj:`Query`): Query object for further customizations
        """

        self.api.op_and(self.query_wrapper_ptr)
        return self

    def op_or(self) -> Query:
        """Next condition will be added with OR.
            Implements short-circuiting:
            if the previous condition is successful the next will not be evaluated, but except Join conditions

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.op_or(self.query_wrapper_ptr)
        return self

    def op_not(self) -> Query:
        """Next condition will be added with NOT AND.
            Implements short-circuiting: if the previous condition is failed the next will not be evaluated

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.op_not(self.query_wrapper_ptr)
        return self

    def request_total(self, total_name: str= '') -> Query:
        """Request total items calculation

        # Arguments:
            total_name (string, optional): Name to be requested

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.request_total(self.query_wrapper_ptr, total_name)
        return self

    def cached_total(self, total_name: str= '') -> Query:
        """Request cached total items calculation

        # Arguments:
            total_name (string, optional): Name to be requested

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.cached_total(self.query_wrapper_ptr, total_name)
        return self

    def limit(self, limit_items: int) -> Query:
        """Set a limit (count) of returned items.
            Analog to sql LIMIT rowsNumber

        # Arguments:
            limit_items (int): Number of rows to get from result set

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.limit(self.query_wrapper_ptr, limit_items)
        return self

    def offset(self, start_offset: int) -> Query:
        """Sets the number of the first selected row from result query

        # Arguments:
            limit_items (int): Index of the first row to get from result set

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.offset(self.query_wrapper_ptr, start_offset)
        return self

    def debug(self, level: int) -> Query:
        """Changes debug level

        # Arguments:
            level (int): Debug level

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.debug(self.query_wrapper_ptr, level)
        return self

    def strict(self, mode: StrictMode) -> Query:
        """Changes strict mode

        # Arguments:
            mode (:enum:`StrictMode`): Strict mode

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.strict(self.query_wrapper_ptr, mode.value)
        return self

    def explain(self) -> Query:
        """Enable explain query

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.explain(self.query_wrapper_ptr)
        return self

    def with_rank(self) -> Query:
        """Output fulltext rank. Allowed only with fulltext query

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.with_rank(self.query_wrapper_ptr)
        return self

################################################################ ToDo
#func (q *Query) SetContext(ctx interface{}) *Query {
#func (q *Query) Exec() *Iterator {
#func (q *Query) ExecCtx(ctx context.Context) *Iterator {
#func (q *Query) ExecToJson(jsonRoots ...string) *JSONIterator {
#func (q *Query) ExecToJsonCtx(ctx context.Context, jsonRoots ...string) *JSONIterator {
#func (q *Query) Delete() (int, error)
#func (q *Query) DeleteCtx(ctx context.Context) (int, error) {
#func (q *Query) SetObject(field string, values interface{}) *Query {
#func (q *Query) Set(field string, values interface{}) *Query {
################################################################

    def drop(self, index: str) -> Query:
        """Drops a value for a field

        # Arguments:
            index (string): Field name for drop operation

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.drop(self.query_wrapper_ptr, index)
        return self

    def expression(self, field: str, value: str) -> Query:
        """Updates indexed field by arithmetical expression

        # Arguments:
            field (string): Field name
            value (string): New value expression for field

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.expression(self.query_wrapper_ptr, field, value)
        return self

################################################################ // ToDo
#func (q *Query) Update() *Iterator {
#func (q *Query) UpdateCtx(ctx context.Context) *Iterator {
#func (q *Query) MustExec() *Iterator {
#func (q *Query) MustExecCtx(ctx context.Context) *Iterator {
#func (q *Query) Get() (item interface{}, found bool) {
#func (q *Query) GetCtx(ctx context.Context) (item interface{}, found bool) {
#func (q *Query) GetJson() (json []byte, found bool) {
#func (q *Query) GetJsonCtx(ctx context.Context) (json []byte, found bool) {
#func (q *Query) InnerJoin(q2 *Query, field string) *Query {
#func (q *Query) Join(q2 *Query, field string) *Query {
#func (q *Query) LeftJoin(q2 *Query, field string) *Query {
#func (q *Query) JoinHandler(field string, handler JoinHandler) *Query {
#func (q *Query) Merge(q2 *Query) *Query {
################################################################

    def on(self, index: str, condition: CondType, join_index: str) -> Query:
        """On specifies join condition.

        # Arguments:
            index (string): Field name from `Query` namespace should be used during join
            condition (:enum:`CondType`): Type of condition, specifies how `Query` will be joined with the latest join query issued on `Query` (e.g. `EQ`/`GT`/`SET`/...)
            join_index (string): Index-field name from namespace for the latest join query issued on `Query` should be used during join

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.on(self.query_wrapper_ptr, index, condition, join_index)
        return self

    def select(self, fields: List[str]) -> Query:
        """Sets list of columns in this namespace to be finally selected.
            The columns should be specified in the same case as the jsonpaths corresponding to them.
            Non-existent fields and fields in the wrong case are ignored.
            If there are no fields in this list that meet these conditions, then the filter works as "*".

        # Arguments:
            fields (list[string]): List of columns to be selected

        # Returns:
            (:obj:`Query`): Query object for further customizations

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code
        """

        self.err_code, self.err_msg = self.api.select_query(self.query_wrapper_ptr, fields)
        self._raise_on_error()
        return self

    def fetch_count(self, n: int) -> Query:
        """Sets the number of items that will be fetched by one operation.
            When n <= 0 query will fetch all results in one operation

        # Arguments:
            n (int): Number of items

        # Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.fetch_count(self.query_wrapper_ptr, n)
        return self

    def functions(self, functions: List[str]) -> Query:
        """Adds sql-functions to query

        # Arguments:
            functions (list[string]): Functions declaration

        # Returns:
            (:obj:`Query`): Query object for further customizations

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code
        """

        self.err_code, self.err_msg = self.api.functions(self.query_wrapper_ptr, functions)
        self._raise_on_error()
        return self

    def equal_position(self, equal_position: List[str]) -> Query:
        """Adds equal position fields to arrays queries

        # Arguments:
            equal_poses (list[string]): Equal position fields to arrays queries

        # Returns:
            (:obj:`Query`): Query object for further customizations

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code
        """

        self.err_code, self.err_msg = self.api.equal_position(self.query_wrapper_ptr, equal_position)
        self._raise_on_error()
        return self

# ToDo 66/33
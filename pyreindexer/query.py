from __future__ import annotations
from typing import List
from enum import Enum

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

class Query(object):
    """ An object representing the context of a Reindexer query

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

################################################################### ToDo
#func (q *Query) Where(index string, condition int, keys interface{}) *Query {
#func (q *Query) WhereQuery(subQuery *Query, condition int, keys interface{}) *Query {
#################################################################

    def where_between_fields(self, first_field: str, condition: CondType, second_field: str) -> Query:
        """Add comparing two fields where condition to DB query

        # Arguments:
            first_field (string): First field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            second_field (string): Second field name used in condition clause

        # Returns:
            (:obj:`Query`): Query object ready to be executed

        """

        self.api.where_between_fields(self.query_wrapper_ptr, first_field, condition.value, second_field)
        return self

    def open_bracket(self) -> Query:
        """Open bracket for where condition to DB query

        # Returns:
            (:obj:`Query`): Query object ready to be executed

        """

        self.api.open_bracket(self.query_wrapper_ptr)
        return self

    def close_bracket(self) -> Query:
        """CloseBracket - Close bracket for where condition to DB query

        # Returns:
            (:obj:`Query`): Query object ready to be executed

        """

        self.api.close_bracket(self.query_wrapper_ptr)
        return self

    def where_int(self, index: str, condition: CondType, keys: List[int]) -> Query:
        """Add where condition to DB query with int args

        # Arguments:
            index (string): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            keys (list[int]): Value of index to be compared with. For composite indexes keys must be list, with value of each subindex

        # Returns:
            (:obj:`Query`): Query object ready to be executed

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.where_int(self.query_wrapper_ptr, index, condition.value, keys)
        self._raise_on_error()
        return self

    def where_int32(self, index: str, condition: CondType, keys: List[int]) -> Query:
        """Add where condition to DB query with Int32 args

        # Arguments:
            index (string): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            keys (list[Int32]): Value of index to be compared with. For composite indexes keys must be list, with value of each subindex

        # Returns:
            (:obj:`Query`): Query object ready to be executed

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.where_int32(self.query_wrapper_ptr, index, condition.value, keys)
        self._raise_on_error()
        return self

    def where_int64(self, index: str, condition: CondType, keys: List[int]) -> Query:
        """Add where condition to DB query with Int64 args

        # Arguments:
            index (string): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            keys (list[Int64]): Value of index to be compared with. For composite indexes keys must be list, with value of each subindex

        # Returns:
            (:obj:`Query`): Query object ready to be executed

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.where_int64(self.query_wrapper_ptr, index, condition.value, keys)
        self._raise_on_error()
        return self

    def where_string(self, index: str, condition: CondType, keys: List[str]) -> Query:
        """Add where condition to DB query with string args

        # Arguments:
            index (string): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            keys (list[string]): Value of index to be compared with. For composite indexes keys must be list, with value of each subindex

        # Returns:
            (:obj:`Query`): Query object ready to be executed

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.where_string(self.query_wrapper_ptr, index, condition.value, keys)
        self._raise_on_error()
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
            (:obj:`Query`): Query object ready to be executed

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.where_uuid(self.query_wrapper_ptr, index, condition.value, keys)
        self._raise_on_error()
        return self

    def where_bool(self, index: str, condition: CondType, keys: List[bool]) -> Query:
        """Add where condition to DB query with bool args

        # Arguments:
            index (string): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            keys (list[bool]): Value of index to be compared with. For composite indexes keys must be list, with value of each subindex

        # Returns:
            (:obj:`Query`): Query object ready to be executed

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.where_bool(self.query_wrapper_ptr, index, condition.value, keys)
        self._raise_on_error()
        return self

    def where_float64(self, index: str, condition: CondType, keys: List[float]) -> Query:
        """Add where condition to DB query with float args

        # Arguments:
            index (string): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            keys (list[float]): Value of index to be compared with. For composite indexes keys must be list, with value of each subindex

        # Returns:
            (:obj:`Query`): Query object ready to be executed

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.where_float64(self.query_wrapper_ptr, index, condition.value, keys)
        self._raise_on_error()
        return self

################################################################ ToDo
#func (q *Query) WhereComposite(index string, condition int, keys ...interface{}) *Query { // ToDo
################################################################

    def match(self, index: str, keys: List[str]) -> Query:
        """Add string EQ-condition to DB query with string args

        # Arguments:
            index (string): Field name used in condition clause
            keys (list[string]): Value of index to be compared with. For composite indexes keys must be list, with value of each subindex

        # Returns:
            (:obj:`Query`): Query object ready to be executed

        # Raises:
            Exception: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.where_string(self.query_wrapper_ptr, index, CondType.CondEq.value, keys)
        self._raise_on_error()
        return self

################################################################ ToDo
#func (q *Query) DWithin(index string, point Point, distance float64) *Query {
#func (q *Query) AggregateSum(field string) *Query {
#func (q *Query) AggregateAvg(field string) *Query {
#func (q *Query) AggregateMin(field string) *Query {
#func (q *Query) AggregateMax(field string) *Query {
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
#            (:obj:`Query`): Query object ready to be executed

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

    def AND(self) -> Query:
        """Next condition will be added with AND.
            This is the default operation for WHERE statement. Do not have to be called explicitly in user's code.
            Used in DSL conversion

        """
        self.api.AND(self.query_wrapper_ptr)
        return self

    def OR(self) -> Query:
        """Next condition will be added with OR.
            Implements short-circuiting:
            if the previous condition is successful the next will not be evaluated, but except Join conditions


        """
        self.api.OR(self.query_wrapper_ptr)
        return self

    def NOT(self) -> Query:
        """Next condition will be added with NOT AND.
            Implements short-circuiting: if the previous condition is failed the next will not be evaluated

        """

        self.api.NOT(self.query_wrapper_ptr)
        return self

################################################################ ToDo
#func (q *Query) Distinct(distinctIndex string) *Query {
#func (q *Query) ReqTotal(totalNames ...string) *Query {
#func (q *Query) CachedTotal(totalNames ...string) *Query {
#func (q *Query) Limit(limitItems int) *Query {
#func (q *Query) Offset(startOffset int) *Query {
#func (q *Query) Debug(level int) *Query {
#func (q *Query) Strict(mode QueryStrictMode) *Query {
#func (q *Query) Explain() *Query {
#func (q *Query) SetContext(ctx interface{}) *Query {
#func (q *Query) Exec() *Iterator {
#func (q *Query) ExecCtx(ctx context.Context) *Iterator {
#func (q *Query) ExecToJson(jsonRoots ...string) *JSONIterator {
#func (q *Query) ExecToJsonCtx(ctx context.Context, jsonRoots ...string) *JSONIterator {
#func (q *Query) Delete() (int, error)
#func (q *Query) DeleteCtx(ctx context.Context) (int, error) {
#func (q *Query) SetObject(field string, values interface{}) *Query {
#func (q *Query) Set(field string, values interface{}) *Query {
#func (q *Query) Drop(field string) *Query {
#func (q *Query) SetExpression(field string, value string) *Query {
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
#func (q *Query) On(index string, condition int, joinIndex string) *Query {
#func (q *Query) Select(fields ...string) *Query {
#func (q *Query) FetchCount(n int) *Query {
#func (q *Query) Functions(fields ...string) *Query {
#func (q *Query) EqualPosition(fields ...string) *Query {
# 66 / 10 + 1 + 3
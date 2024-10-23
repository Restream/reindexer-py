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

    """

    def __init__(self, api, query_wrapper_ptr):
        """Constructs a new Reindexer query object

        # Arguments:
            api (module): An API module for Reindexer calls
            query_wrapper_ptr (int): A memory pointer to Reindexer query object

        """

        self.api = api
        self.query_wrapper_ptr = query_wrapper_ptr

    def __del__(self):
        """Free query memory

        """

        if self.query_wrapper_ptr > 0:
            self.api.delete_query(self.query_wrapper_ptr)

    def Where(self, index: str, condition: CondType, keys: List[str]):
        """Where - Add where condition to DB query

        # Arguments:
            index (string): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            keys (list[string]): Value of index to be compared with. For composite indexes keys must be list, with value of each subindex

        #Returns:
            (:obj:`Query`): Query object ready to be executed

        """

        return self

#func (q *Query) WhereQuery(subQuery *Query, condition int, keys interface{}) *Query {
#func (q *Query) WhereBetweenFields(firstField string, condition int, secondField string) *Query {
#func (q *Query) OpenBracket() *Query {
#func (q *Query) CloseBracket() *Query {
#func (q *Query) WhereInt(index string, condition int, keys ...int) *Query {
#func (q *Query) WhereInt32(index string, condition int, keys ...int32) *Query {
#func (q *Query) WhereInt64(index string, condition int, keys ...int64) *Query {
#func (q *Query) WhereString(index string, condition int, keys ...string) *Query {
#func (q *Query) WhereUuid(index string, condition int, keys ...string) *Query {
#func (q *Query) WhereComposite(index string, condition int, keys ...interface{}) *Query {
#func (q *Query) Match(index string, keys ...string) *Query {
#func (q *Query) WhereBool(index string, condition int, keys ...bool) *Query {
#func (q *Query) WhereDouble(index string, condition int, keys ...float64) *Query {
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
#func (q *Query) SortStFieldDistance(field1 string, field2 string, desc bool) *Query {
#func (q *Query) And() *Query {
#func (q *Query) Or() *Query {
#func (q *Query) Not() *Query {
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

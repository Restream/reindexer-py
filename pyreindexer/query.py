from __future__ import annotations

from collections.abc import Iterable
from datetime import timedelta
from enum import Enum
from typing import Optional, Union
from uuid import UUID

from pyreindexer.exceptions import ApiError, QueryError
from pyreindexer.query_results import QueryResults
from pyreindexer.point import Point


class ExtendedEnum(Enum):

    def __eq__(self, other):
        return self.value == other


class CondType(ExtendedEnum):
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


class StrictMode(ExtendedEnum):
    NotSet = 0
    Empty = 1
    Names = 2
    Indexes = 3


class JoinType(ExtendedEnum):
    LeftJoin = 0
    InnerJoin = 1
    OrInnerJoin = 2
    Merge = 3


class LogLevel(ExtendedEnum):
    Off = 0
    Error = 1
    Warning = 2
    Info = 3
    Trace = 4


simple_types = Union[int, str, bool, float]


class Query:
    """An object representing the context of a Reindexer query

    #### Attributes:
        api (module): An API module for Reindexer calls
        query_wrapper_ptr (int): A memory pointer to Reindexer query object
        err_code (int): The API error code
        err_msg (string): The API error message
        root (:object: Optional[`Query`]): The root query of the Reindexer query
        join_queries (list[:object:`Query`]): The list of join Reindexer query objects
        merged_queries (list[:object:`Query`]): The list of merged Reindexer query objects

    """

    def __init__(self, api, query_wrapper_ptr: int):
        """Constructs a new Reindexer query object

        #### Arguments:
            api (module): An API module for Reindexer calls
            query_wrapper_ptr (int): A memory pointer to Reindexer query object

        """

        self.api = api
        self.query_wrapper_ptr: int = query_wrapper_ptr
        self.err_code: int = 0
        self.err_msg: str = ''
        self.root: Optional[Query] = None
        self.join_queries: list[Query] = []
        self.merged_queries: list[Query] = []

    def __del__(self):
        """Frees query memory

        """

        if self.query_wrapper_ptr > 0:
            self.api.destroy_query(self.query_wrapper_ptr)

    def __raise_on_error(self) -> None:
        """Checks if there is an error code and raises with an error message

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        if self.err_code:
            raise ApiError(self.err_msg)

    @staticmethod
    def __convert_to_list(param: Union[simple_types, tuple[list[simple_types], ...]]) -> list:
        """Converts an input parameter to a list of lists

        #### Arguments:
            param (union[simple_types, (list[simple_types], ...)]): The input parameter

        #### Returns:
            list[union[union[int, bool, float, str], list[union[int, bool, float, str]]]:
                Always converted to a list of lists

        """

        if param is None:
            return []

        if isinstance(param, str) or not isinstance(param, Iterable):
            return [param]

        if isinstance(param, list):
            return param

        result = list(param)
        if len(result) == 0 or not isinstance(result[0], list):
            result: list = [result]
        return result

    @staticmethod
    def __convert_strs_to_list(param: tuple[str, ...]) -> list[str]:
        """Converts an input parameter to a list

        #### Arguments:
            param (tuple[string, ...]): The input parameter

        #### Returns:
            list[string]: Always converted to a list

        """

        return [] if param is None else list(param)

    def __where(self, index: str, condition: CondType,
                keys: Union[simple_types, tuple[list[simple_types], ...]]) -> Query:
        """Adds where condition to DB query with args

        #### Arguments:
            index (string): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            keys (union[simple_types, (list[simple_types], ...)]):
                Value of index to be compared with. For composite indexes keys must be list,
                with value of each sub-index

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            QueryError: Raises with an error message if inappropriate condition is used
            ApiError: Raises with an error message of API return on non-zero error code

        """

        if condition == CondType.CondDWithin:
            raise QueryError("In this case, use a special method 'dwithin'")

        params = self.__convert_to_list(keys)

        self.err_code, self.err_msg = self.api.where(self.query_wrapper_ptr, index, condition.value, params)
        self.__raise_on_error()
        return self

    def where(self, index: str, condition: CondType,
              keys: Union[simple_types, tuple[list[simple_types], ...]] = None) -> Query:
        """Adds where condition to DB query with args

        #### Arguments:
            index (string): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            keys (union[simple_types, (list[simple_types], ...)]):
                Value of index to be compared with. For composite indexes keys must be list,
                with value of each sub-index

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        return self.__where(index, condition, keys)

    def where_query(self, sub_query: Query, condition: CondType,
                    keys: Union[simple_types, tuple[list[simple_types], ...]] = None) -> Query:
        """Adds sub-query where condition to DB query with args

        #### Arguments:
            sub_query (:obj:`Query`): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            keys (union[simple_types, (list[simple_types], ...)]):
                Value of index to be compared with. For composite indexes keys must be list,
                with value of each sub-index

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        params = self.__convert_to_list(keys)

        self.err_code, self.err_msg = self.api.where_subquery(self.query_wrapper_ptr, sub_query.query_wrapper_ptr,
                                                              condition.value, params)
        self.__raise_on_error()
        return self

    def where_subquery(self, index: str, condition: CondType, sub_query: Query) -> Query:
        """Adds sub-query where condition to DB query

        #### Arguments:
            index (string): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            sub_query (:obj:`Query`): Field name used in condition clause

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.where_field_subquery(self.query_wrapper_ptr, index, condition.value, sub_query.query_wrapper_ptr)
        return self

    def where_composite(self, index: str, condition: CondType, keys: tuple[list[simple_types], ...]) -> Query:
        """Adds where condition to DB query with interface args for composite indexes

        #### Arguments:
            index (string): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            keys (list[simple_types], ...): Values of composite index to be compared with (value of each sub-index).
                Supported variants:
                    ([1, "test1"], [2, "test2"])
                    [[1, "test1"], [2, "test2"]])
                    ([1, "testval1"], )
                    [[1, "testval1"]]
                    (1, "testval1")

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        return self.__where(index, condition, keys)

    def where_uuid(self, index: str, condition: CondType, *uuids: UUID) -> Query:
        """Adds where condition to DB query with UUID as string args.
            This function applies binary encoding to the UUID value.
            `index` MUST be declared as uuid index in this case

        #### Arguments:
            index (string): Field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            uuids (*:obj:`UUID`): Value of index to be compared with. For composite indexes uuids must be list,
                with value of each sub-index

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        params: list[str] = []
        for item in uuids:
            params.append(str(item))

        self.err_code, self.err_msg = self.api.where_uuid(self.query_wrapper_ptr, index, condition.value, params)
        self.__raise_on_error()
        return self

    def where_between_fields(self, first_field: str, condition: CondType, second_field: str) -> Query:
        """Adds comparing two fields where condition to DB query

        #### Arguments:
            first_field (string): First field name used in condition clause
            condition (:enum:`CondType`): Type of condition
            second_field (string): Second field name used in condition clause

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.where_between_fields(self.query_wrapper_ptr, first_field, condition.value, second_field)
        return self

    def open_bracket(self) -> Query:
        """Opens bracket for where condition to DB query

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.open_bracket(self.query_wrapper_ptr)
        self.__raise_on_error()
        return self

    def close_bracket(self) -> Query:
        """Closes bracket for where condition to DB query

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        self.err_code, self.err_msg = self.api.close_bracket(self.query_wrapper_ptr)
        self.__raise_on_error()
        return self

    def match(self, index: str, *keys: str) -> Query:
        """Adds string EQ-condition to DB query with string args

        #### Arguments:
            index (string): Field name used in condition clause
            keys (*string): Value of index to be compared with. For composite indexes keys must be list,
                with value of each sub-index

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        params: list = self.__convert_strs_to_list(keys)

        self.err_code, self.err_msg = self.api.where(self.query_wrapper_ptr, index, CondType.CondEq.value, params)
        self.__raise_on_error()
        return self

    def dwithin(self, index: str, point: Point, distance: float) -> Query:
        """Adds DWithin condition to DB query

        #### Arguments:
            index (string): Field name used in condition clause
            point (:obj:`Point`): Point object used in condition clause
            distance (float): Distance in meters between point

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.dwithin(self.query_wrapper_ptr, index, point.x, point.y, distance)
        return self

    def distinct(self, index: str) -> Query:
        """Performs distinct for a certain index. Return only items with uniq value of field

        #### Arguments:
            index (string): Field name for distinct operation

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.aggregate_distinct(self.query_wrapper_ptr, index)
        return self

    def aggregate_sum(self, index: str) -> Query:
        """Performs a summation of values for a specified index

        #### Arguments:
            index (string): Field name for sum operation

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.aggregate_sum(self.query_wrapper_ptr, index)
        return self

    def aggregate_avg(self, index: str) -> Query:
        """Finds for the average at the specified index

        #### Arguments:
            index (string): Field name for sum operation

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.aggregate_avg(self.query_wrapper_ptr, index)
        return self

    def aggregate_min(self, index: str) -> Query:
        """Finds for the minimum at the specified index

        #### Arguments:
            index (string): Field name for sum operation

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.aggregate_min(self.query_wrapper_ptr, index)
        return self

    def aggregate_max(self, index: str) -> Query:
        """Finds for the maximum at the specified index

        #### Arguments:
            index (string): Field name for sum operation

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.aggregate_max(self.query_wrapper_ptr, index)
        return self

    class _AggregateFacet:
        """An object representing the context of a Reindexer aggregate facet

        #### Attributes:
            api (module): An API module for Reindexer calls
            query_wrapper_ptr (int): A memory pointer to Reindexer query object

        """

        def __init__(self, query: Query):
            """Constructs a new Reindexer AggregateFacetRequest object

            #### Arguments:
                (:obj:`Query`): Query object for further customizations

            """

            self.api = query.api
            self.query_wrapper_ptr = query.query_wrapper_ptr

        def limit(self, limit: int) -> Query._AggregateFacet:
            """Limits facet aggregation results

            #### Arguments:
                limit (int): Limit of aggregation of facet

            #### Returns:
                (:obj:`_AggregateFacet`): Facet object for further customizations

            """

            self.api.aggregation_limit(self.query_wrapper_ptr, limit)
            return self

        def offset(self, offset: int) -> Query._AggregateFacet:
            """Sets offset of the facet aggregation results

            #### Arguments:
                limit (int): Offset in facet aggregation results

            #### Returns:
                (:obj:`_AggregateFacet`): Facet object for further customizations

            """

            self.api.aggregation_offset(self.query_wrapper_ptr, offset)
            return self

        def sort(self, field: str, desc: bool = False) -> Query._AggregateFacet:
            """Sorts facets by field value

            #### Arguments:
                field (str): Item field. Use field `count` to sort by facet's count value
                desc (bool): Sort in descending order flag

            #### Returns:
                (:obj:`_AggregateFacet`): Facet object for further customizations

            """

            self.api.aggregation_sort(self.query_wrapper_ptr, field, desc)
            return self

    def aggregate_facet(self, *fields: str) -> Query._AggregateFacet:
        """Gets fields facet value. Applicable to multiple data fields and the result of that could be sorted
            by any data column or `count` and cut off by offset and limit. In order to support this functionality
            this method returns AggregationFacetRequest which has methods sort, limit and offset

        #### Arguments:
            fields (*string): Fields any data column name or `count`, fields should not be empty

        #### Returns:
            (:obj:`_AggregateFacet`): Request object for further customizations

        """

        params: list = self.__convert_strs_to_list(fields)

        self.err_code, self.err_msg = self.api.aggregation(self.query_wrapper_ptr, params)
        self.__raise_on_error()
        return self._AggregateFacet(self)

    def sort(self, index: str, desc: bool = False,
             forced_sort_values: Union[simple_types, tuple[list[simple_types], ...]] = None) -> Query:
        """Applies sort order to return from query items. If forced_sort_values argument specified, then items equal to
            values, if found will be placed in the top positions. Forced sort is support for the first sorting field
            only

        #### Arguments:
            index (string): The index name
            desc (bool): Sort in descending order
            forced_sort_values (union[simple_types, (list[simple_types], ...)]):
                Value of index to match. For composite indexes keys must be list, with value of each sub-index

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        values = self.__convert_to_list(forced_sort_values)

        self.err_code, self.err_msg = self.api.sort(self.query_wrapper_ptr, index, desc, values)
        self.__raise_on_error()
        return self

    def sort_stpoint_distance(self, index: str, point: Point, desc: bool) -> Query:
        """Applies geometry sort order to return from query items. Wrapper for geometry sorting by shortest distance
            between geometry field and point (ST_Distance)

        #### Arguments:
            index (string): The index name
            point (:obj:`Point`): Point object used in sorting operation
            desc (bool): Sort in descending order

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        request: str = f"ST_Distance({index},ST_GeomFromText('point({point.x:.12f} {point.y:.12f})'))"
        return self.sort(request, desc)

    def sort_stfield_distance(self, first_field: str, second_field: str, desc: bool) -> Query:
        """Applies geometry sort order to return from query items. Wrapper for geometry sorting by shortest distance
            between 2 geometry fields (ST_Distance)

        #### Arguments:
            first_field (string): First field name used in condition
            second_field (string): Second field name used in condition
            desc (bool): Sort in descending order

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        request: str = f"ST_Distance({first_field},{second_field})"
        return self.sort(request, desc)

    def op_and(self) -> Query:
        """Next condition will be added with AND.
            This is the default operation for WHERE statement. Do not have to be called explicitly in user's code.
            Used in DSL conversion

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.op_and(self.query_wrapper_ptr)
        return self

    def op_or(self) -> Query:
        """Next condition will be added with OR.
            Implements short-circuiting:
            if the previous condition is successful the next will not be evaluated, but except Join conditions

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.op_or(self.query_wrapper_ptr)
        return self

    def op_not(self) -> Query:
        """Next condition will be added with NOT AND.
            Implements short-circuiting: if the previous condition is failed the next will not be evaluated

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.op_not(self.query_wrapper_ptr)
        return self

    def request_total(self) -> Query:
        """Requests total items calculation

        #### Arguments:
            total_name (string, optional): Name to be requested

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.request_total(self.query_wrapper_ptr)
        return self

    def cached_total(self) -> Query:
        """Requests cached total items calculation

        #### Arguments:
            total_name (string, optional): Name to be requested

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.cached_total(self.query_wrapper_ptr)
        return self

    def limit(self, limit_items: int) -> Query:
        """Sets a limit (count) of returned items. Analog to sql LIMIT rowsNumber

        #### Arguments:
            limit_items (int): Number of rows to get from result set

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.limit(self.query_wrapper_ptr, limit_items)
        return self

    def offset(self, start_offset: int) -> Query:
        """Sets the number of the first selected row from result query

        #### Arguments:
            limit_items (int): Index of the first row to get from result set

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.offset(self.query_wrapper_ptr, start_offset)
        return self

    def debug(self, level: LogLevel) -> Query:
        """Changes debug log level on server

        #### Arguments:
            level (:enum:`LogLevel`): Debug log level on server

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.debug(self.query_wrapper_ptr, level.value)
        return self

    def strict(self, mode: StrictMode) -> Query:
        """Changes strict mode

        #### Arguments:
            mode (:enum:`StrictMode`): Strict mode

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.strict(self.query_wrapper_ptr, mode.value)
        return self

    def explain(self) -> Query:
        """Enables explain query

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.explain(self.query_wrapper_ptr)
        return self

    def with_rank(self) -> Query:
        """Outputs fulltext rank. Allowed only with fulltext query

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.with_rank(self.query_wrapper_ptr)
        return self

    def execute(self, timeout: timedelta = timedelta(milliseconds=0)) -> QueryResults:
        """Executes a select query

        #### Arguments:
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Returns:
            (:obj:`QueryResults`): A QueryResults iterator

        #### Raises:
            ApiError: Raises with an error message when query is in an invalid state
            ApiError: Raises with an error message of API return on non-zero error code

        """

        if self.root is not None:
            return self.root.execute(timeout)

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        (self.err_code, self.err_msg,
         wrapper_ptr, iter_count, total_count) = self.api.select_query(self.query_wrapper_ptr, milliseconds)
        self.__raise_on_error()
        return QueryResults(self.api, wrapper_ptr, iter_count, total_count)

    def delete(self, timeout: timedelta = timedelta(milliseconds=0)) -> int:
        """Executes a query, and delete items, matches query

        #### Arguments:
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Returns:
            (int): Number of deleted elements

        #### Raises:
            QueryError: Raises with an error message when query is in an invalid state
            ApiError: Raises with an error message of API return on non-zero error code

        """

        if (self.root is not None) or (len(self.join_queries) > 0):
            raise QueryError("Delete does not support joined queries")

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        self.err_code, self.err_msg, number = self.api.delete_query(self.query_wrapper_ptr, milliseconds)
        self.__raise_on_error()
        return number

    def set_object(self, field: str, values: list[simple_types]) -> Query:
        """Adds an update query to an object field for an update query

        #### Arguments:
            field (string): Field name
            values (list[simple_types]): List of values to add

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            QueryError: Raises with an error message if no values are specified
            ApiError: Raises with an error message of API return on non-zero error code

        """

        if values is None:
            raise QueryError("A required parameter is not specified. `values` can't be None")

        self.err_code, self.err_msg = self.api.set_object(self.query_wrapper_ptr, field, values)
        self.__raise_on_error()
        return self

    def set(self, field: str, values: list[simple_types]) -> Query:
        """Adds a field update request to the update request

        #### Arguments:
            field (string): Field name
            values (list[simple_types]): List of values to add

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        values = [] if values is None else values

        self.err_code, self.err_msg = self.api.set(self.query_wrapper_ptr, field, values)
        self.__raise_on_error()
        return self

    def drop(self, index: str) -> Query:
        """Drops a value for a field

        #### Arguments:
            index (string): Field name for drop operation

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.drop(self.query_wrapper_ptr, index)
        return self

    def expression(self, field: str, value: str) -> Query:
        """Updates indexed field by arithmetical expression

        #### Arguments:
            field (string): Field name
            value (string): New value expression for field

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        self.api.expression(self.query_wrapper_ptr, field, value)
        return self

    def update(self, timeout: timedelta = timedelta(milliseconds=0)) -> QueryResults:
        """Executes update query, and update fields in items, which matches query

        #### Arguments:
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Returns:
            (:obj:`QueryResults`): A QueryResults iterator

        #### Raises:
            QueryError: Raises with an error message when query is in an invalid state
            ApiError: Raises with an error message of API return on non-zero error code

        """

        if (self.root is not None) or (len(self.join_queries) > 0):
            raise QueryError("Update does not support joined queries")

        milliseconds: int = int(timeout / timedelta(milliseconds=1))
        (self.err_code, self.err_msg,
         wrapper_ptr, iter_count, total_count) = self.api.update_query(self.query_wrapper_ptr, milliseconds)
        self.__raise_on_error()
        return QueryResults(self.api, wrapper_ptr, iter_count, total_count)

    def must_execute(self, timeout: timedelta = timedelta(milliseconds=0)) -> QueryResults:
        """Executes a query, and update fields in items, which matches query, with status check

        #### Arguments:
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Returns:
            (:obj:`QueryResults`): A QueryResults iterator

        #### Raises:
            ApiError: Raises with an error message when query is in an invalid state
            ApiError: Raises with an error message of API return on non-zero error code

        """

        result = self.execute(timeout)
        result.status()
        return result

    def get(self, timeout: timedelta = timedelta(milliseconds=0)) -> (str, bool):
        """Executes a query, and return 1 JSON item

        #### Arguments:
            timeout (`datetime.timedelta`): Optional timeout for performing a server-side operation.
                Minimum 1 millisecond, if set to a value less, it corresponds to disabling the timeout.
                A value of 0 disables the timeout (default value)

        #### Returns:
            (:tuple:string,bool): 1st string item and found flag

        #### Raises:
            ApiError: Raises with an error message when query is in an invalid state
            ApiError: Raises with an error message of API return on non-zero error code

        """

        if self.root is not None:
            return self.get()

        selected_items = self.limit(1).must_execute(timeout)
        for item in selected_items:
            return item, True

        return '', False

    def __join(self, query: Query, field: str, join_type: JoinType) -> Query:
        """Joins queries

        #### Arguments:
            query (:obj:`Query`): Query object to join
            field (string): Joined field name
            type (:enum:`JoinType`): Join type

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            Exception: Raises with an error message when query is in an invalid state

        """

        if self.root is not None:
            return self.root.__join(query, field, join_type)

        if query.root is not None:
            raise QueryError("Query.join call on already joined query. You should create new Query")

        # index of join query
        self.api.join(self.query_wrapper_ptr, join_type.value, query.query_wrapper_ptr)

        query.root = self
        self.join_queries.append(query)
        return query

    def inner_join(self, query: Query, field: str) -> Query:
        """Joins 2 queries.
            Items from the 1-st query are filtered by and expanded with the data from the 2-nd query

        #### Arguments:
            query (:obj:`Query`): Query object to left join
            field (string): Joined field name. As unique identifier for the join between this query and `join_query`.
                Parameter in order for InnerJoin to work: namespace of `query` contains `field` as one of its fields
                marked as `joined`

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        return self.__join(query, field, JoinType.InnerJoin)

    def join(self, query: Query, field: str) -> Query:
        """Join is an alias for LeftJoin. Joins 2 queries.
            Items from this query are expanded with the data from the `query`

        #### Arguments:
            query (:obj:`Query`): Query object to left join
            field (string): Joined field name. As unique identifier for the join between this query and `join_query`

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        return self.__join(query, field, JoinType.LeftJoin)

    def left_join(self, join_query: Query, field: str) -> Query:
        """Joins 2 queries.
            Items from this query are expanded with the data from the join_query.
            One of the conditions below must hold for `field` parameter in order for LeftJoin to work:
                namespace of `join_query` contains `field` as one of its fields marked as `joined`

        #### Arguments:
            query (:obj:`Query`): Query object to left join
            field (string): Joined field name. As unique identifier for the join between this query and `join_query`

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        return self.__join(join_query, field, JoinType.LeftJoin)

    def merge(self, query: Query) -> Query:
        """Merges queries of the same type

        #### Arguments:
            query (:obj:`Query`): Query object to merge

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        """

        if self.root is not None:
            return self.root.merge(query)

        if query.root is not None:
            query = query.root

        query.root = self
        self.merged_queries.append(query)
        self.api.merge(self.query_wrapper_ptr, query.query_wrapper_ptr)
        return self

    def on(self, index: str, condition: CondType, join_index: str) -> Query:
        """On specifies join condition

        #### Arguments:
            index (string): Field name from `Query` namespace should be used during join
            condition (:enum:`CondType`): Type of condition, specifies how `Query` will be joined with the latest join query issued on `Query` (e.g. `EQ`/`GT`/`SET`/...)
            join_index (string): Index-field name from namespace for the latest join query issued on `Query` should be used during join

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            QueryError: Raises with an error message when query is in an invalid state

        """

        if self.root is None:
            raise QueryError("Can't join on root query")

        self.api.on(self.query_wrapper_ptr, index, condition.value, join_index)
        return self

    def select(self, *fields: str) -> Query:
        """Sets list of columns in this namespace to be finally selected.
            The columns should be specified in the same case as the jsonpaths corresponding to them.
            Non-existent fields and fields in the wrong case are ignored.
            If there are no fields in this list that meet these conditions, then the filter works as "*"

        #### Arguments:
            fields (*string): List of columns to be selected

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        keys: list = self.__convert_strs_to_list(fields)

        self.err_code, self.err_msg = self.api.select_filter(self.query_wrapper_ptr, keys)
        self.__raise_on_error()
        return self

    def functions(self, *functions: str) -> Query:
        """Adds sql-functions to query

        #### Arguments:
            functions (*string): Functions declaration

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        funcs: list = self.__convert_strs_to_list(functions)

        self.err_code, self.err_msg = self.api.functions(self.query_wrapper_ptr, funcs)
        self.__raise_on_error()
        return self

    def equal_position(self, *equal_position: str) -> Query:
        """Adds equal position fields to arrays queries

        #### Arguments:
            equal_poses (*string): Equal position fields to arrays queries

        #### Returns:
            (:obj:`Query`): Query object for further customizations

        #### Raises:
            ApiError: Raises with an error message of API return on non-zero error code

        """

        equal_pos: list = self.__convert_strs_to_list(equal_position)

        self.err_code, self.err_msg = self.api.equal_position(self.query_wrapper_ptr, equal_pos)
        self.__raise_on_error()
        return self

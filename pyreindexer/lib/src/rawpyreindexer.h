#pragma once

#ifdef PYREINDEXER_CPROTO
#define MODULE_NAME "RawPyReindexer_cproto"
#define MODULE_DESCRIPTION "A cproto connector that allows to interact with Reindexer from Python"
#define MODULE_EXPORT_FUNCTION PyInit_rawpyreindexerc
#else
#define MODULE_NAME "RawPyReindexer_builtin"
#define MODULE_DESCRIPTION "A builtin connector that allows to interact with Reindexer from Python"
#define MODULE_EXPORT_FUNCTION PyInit_rawpyreindexerb
#endif

#include <Python.h>

namespace pyreindexer {

// common
static PyObject* Init(PyObject* self, PyObject* args);
static PyObject* Destroy(PyObject* self, PyObject* args);
static PyObject* Connect(PyObject* self, PyObject* args);
static PyObject* Select(PyObject* self, PyObject* args);
// namespace
static PyObject* NamespaceOpen(PyObject* self, PyObject* args);
static PyObject* NamespaceClose(PyObject* self, PyObject* args);
static PyObject* NamespaceDrop(PyObject* self, PyObject* args);
static PyObject* EnumNamespaces(PyObject* self, PyObject* args);
// index
static PyObject* IndexAdd(PyObject* self, PyObject* args);
static PyObject* IndexUpdate(PyObject* self, PyObject* args);
static PyObject* IndexDrop(PyObject* self, PyObject* args);
// item
static PyObject* ItemInsert(PyObject* self, PyObject* args);
static PyObject* ItemUpdate(PyObject* self, PyObject* args);
static PyObject* ItemUpsert(PyObject* self, PyObject* args);
static PyObject* ItemDelete(PyObject* self, PyObject* args);
// meta
static PyObject* PutMeta(PyObject* self, PyObject* args);
static PyObject* GetMeta(PyObject* self, PyObject* args);
static PyObject* DeleteMeta(PyObject* self, PyObject* args);
static PyObject* EnumMeta(PyObject* self, PyObject* args);
// query results
static PyObject* QueryResultsWrapperStatus(PyObject* self, PyObject* args);
static PyObject* QueryResultsWrapperIterate(PyObject* self, PyObject* args);
static PyObject* QueryResultsWrapperDelete(PyObject* self, PyObject* args);
static PyObject* GetAggregationResults(PyObject* self, PyObject* args);
static PyObject* GetExplainResults(PyObject* self, PyObject* args);
// transaction (sync)
static PyObject* NewTransaction(PyObject* self, PyObject* args);
static PyObject* InsertTransaction(PyObject* self, PyObject* args);
static PyObject* UpdateTransaction(PyObject* self, PyObject* args);
static PyObject* UpsertTransaction(PyObject* self, PyObject* args);
static PyObject* DeleteTransaction(PyObject* self, PyObject* args);
static PyObject* CommitTransaction(PyObject* self, PyObject* args);
static PyObject* RollbackTransaction(PyObject* self, PyObject* args);
// query
static PyObject* CreateQuery(PyObject* self, PyObject* args);
static PyObject* DestroyQuery(PyObject* self, PyObject* args);
static PyObject* Where(PyObject* self, PyObject* args);
static PyObject* WhereSubQuery(PyObject* self, PyObject* args);
static PyObject* WhereFieldSubQuery(PyObject* self, PyObject* args);
static PyObject* WhereUUID(PyObject* self, PyObject* args);
static PyObject* WhereBetweenFields(PyObject* self, PyObject* args);
static PyObject* OpenBracket(PyObject* self, PyObject* args);
static PyObject* CloseBracket(PyObject* self, PyObject* args);
static PyObject* DWithin(PyObject* self, PyObject* args);
static PyObject* AggregateDistinct(PyObject* self, PyObject* args);
static PyObject* AggregateSum(PyObject* self, PyObject* args);
static PyObject* AggregateAvg(PyObject* self, PyObject* args);
static PyObject* AggregateMin(PyObject* self, PyObject* args);
static PyObject* AggregateMax(PyObject* self, PyObject* args);
static PyObject* AggregationLimit(PyObject* self, PyObject* args);
static PyObject* AggregationOffset(PyObject* self, PyObject* args);
static PyObject* AggregationSort(PyObject* self, PyObject* args);
static PyObject* Aggregation(PyObject* self, PyObject* args);
static PyObject* Sort(PyObject* self, PyObject* args);
static PyObject* And(PyObject* self, PyObject* args);
static PyObject* Or(PyObject* self, PyObject* args);
static PyObject* Not(PyObject* self, PyObject* args);
static PyObject* ReqTotal(PyObject* self, PyObject* args);
static PyObject* CachedTotal(PyObject* self, PyObject* args);
static PyObject* Limit(PyObject* self, PyObject* args);
static PyObject* Offset(PyObject* self, PyObject* args);
static PyObject* Debug(PyObject* self, PyObject* args);
static PyObject* Strict(PyObject* self, PyObject* args);
static PyObject* Explain(PyObject* self, PyObject* args);
static PyObject* WithRank(PyObject* self, PyObject* args);
static PyObject* SelectQuery(PyObject* self, PyObject* args);
static PyObject* DeleteQuery(PyObject* self, PyObject* args);
static PyObject* UpdateQuery(PyObject* self, PyObject* args);
static PyObject* SetObject(PyObject* self, PyObject* args);
static PyObject* Set(PyObject* self, PyObject* args);
static PyObject* Drop(PyObject* self, PyObject* args);
static PyObject* SetExpression(PyObject* self, PyObject* args);
static PyObject* Join(PyObject* self, PyObject* args);
static PyObject* Merge(PyObject* self, PyObject* args);
static PyObject* On(PyObject* self, PyObject* args);
static PyObject* SelectFilter(PyObject* self, PyObject* args);
static PyObject* AddFunctions(PyObject* self, PyObject* args);
static PyObject* AddEqualPosition(PyObject* self, PyObject* args);

// clang-format off
static PyMethodDef module_methods[] = {
	{"init", Init, METH_VARARGS, "init reindexer instance"},
	{"destroy", Destroy, METH_VARARGS, "destroy reindexer instance"},
	{"connect", Connect, METH_VARARGS, "connect to reindexer database"},
	{"select", Select, METH_VARARGS, "select query"},
	// namespace
	{"namespace_open", NamespaceOpen, METH_VARARGS, "open namespace"},
	{"namespace_close", NamespaceClose, METH_VARARGS, "close namespace"},
	{"namespace_drop", NamespaceDrop, METH_VARARGS, "drop namespace"},
	{"namespaces_enum", EnumNamespaces, METH_VARARGS, "enum namespaces"},
	// index
	{"index_add", IndexAdd, METH_VARARGS, "add index"},
	{"index_update", IndexUpdate, METH_VARARGS, "update index"},
	{"index_drop", IndexDrop, METH_VARARGS, "drop index"},
	// item
	{"item_insert", ItemInsert, METH_VARARGS, "insert item"},
	{"item_update", ItemUpdate, METH_VARARGS, "update item"},
	{"item_upsert", ItemUpsert, METH_VARARGS, "upsert item"},
	{"item_delete", ItemDelete, METH_VARARGS, "delete item"},
	// meta
	{"meta_put", PutMeta, METH_VARARGS, "put meta"},
	{"meta_get", GetMeta, METH_VARARGS, "get meta"},
	{"meta_delete", DeleteMeta, METH_VARARGS, "delete meta"},
	{"meta_enum", EnumMeta, METH_VARARGS, "enum meta"},
	// query results
	{"query_results_status", QueryResultsWrapperStatus, METH_VARARGS, "get query result status"},
	{"query_results_iterate", QueryResultsWrapperIterate, METH_VARARGS, "get query result"},
	{"query_results_delete", QueryResultsWrapperDelete, METH_VARARGS, "free query results buffer"},
	{"get_agg_results", GetAggregationResults, METH_VARARGS, "get aggregation results"},
	{"get_explain_results", GetExplainResults, METH_VARARGS, "get explain results"},
	// transaction (sync)
	{"new_transaction", NewTransaction, METH_VARARGS, "start new transaction"},
	{"item_insert_transaction", InsertTransaction, METH_VARARGS, "item insert transaction"},
	{"item_update_transaction", UpdateTransaction, METH_VARARGS, "item update transaction"},
	{"item_upsert_transaction", UpsertTransaction, METH_VARARGS, "item upsert transaction"},
	{"item_delete_transaction", DeleteTransaction, METH_VARARGS, "item delete transaction"},
	{"commit_transaction", CommitTransaction, METH_VARARGS, "apply changes. Free transaction object memory"},
	{"rollback_transaction", RollbackTransaction, METH_VARARGS, "rollback changes. Free transaction object memory"},
	// query
	{"create_query", CreateQuery, METH_VARARGS, "create new query"},
	{"destroy_query", DestroyQuery, METH_VARARGS, "delete query object. Free query object memory"},
	{"where", Where, METH_VARARGS, "add where condition with args"},
	{"where_subquery", WhereSubQuery, METH_VARARGS, "add sub-query where condition"},
	{"where_field_subquery", WhereFieldSubQuery, METH_VARARGS, "add where condition for sub-query"},
	{"where_uuid", WhereUUID, METH_VARARGS, "add where condition with UUIDs"},
	{"where_between_fields", WhereBetweenFields, METH_VARARGS, "add comparing two fields where condition"},
	{"open_bracket", OpenBracket, METH_VARARGS, "open bracket for where condition"},
	{"close_bracket", CloseBracket, METH_VARARGS, "close bracket for where condition"},
	{"dwithin", DWithin, METH_VARARGS, "add dwithin condition"},
	{"aggregate_distinct", AggregateDistinct, METH_VARARGS, "list of unique values of field"},
	{"aggregate_sum", AggregateSum, METH_VARARGS, "sum field value"},
	{"aggregate_avg", AggregateAvg, METH_VARARGS, "average field value"},
	{"aggregate_min", AggregateMin, METH_VARARGS, "minimum field value"},
	{"aggregate_max", AggregateMax, METH_VARARGS, "maximum field value"},
	{"aggregation_limit", AggregationLimit, METH_VARARGS, "limit facet results"},
	{"aggregation_offset", AggregationOffset, METH_VARARGS, "set offset for facet results"},
	{"aggregation_sort", AggregationSort, METH_VARARGS, "sort facets"},
	{"aggregation", Aggregation, METH_VARARGS, "get fields facet value"},
	{"sort", Sort, METH_VARARGS, "apply sort order"},
	{"op_and", And, METH_VARARGS, "next condition will be added with AND AND"},
	{"op_or", Or, METH_VARARGS, "next condition will be added with OR AND"},
	{"op_not", Not, METH_VARARGS, "next condition will be added with NOT AND"},
	{"request_total", ReqTotal, METH_VARARGS, "request total items calculation"},
	{"cached_total", CachedTotal, METH_VARARGS, "request cached total items calculation"},
	{"limit", Limit, METH_VARARGS, "request cached total items calculation"},
	{"offset", Offset, METH_VARARGS, "request cached total items calculation"},
	{"debug", Debug, METH_VARARGS, "request cached total items calculation"},
	{"strict", Strict, METH_VARARGS, "request cached total items calculation"},
	{"explain", Explain, METH_VARARGS, "enable explain query"},
	{"with_rank", WithRank, METH_VARARGS, "enable fulltext rank"},
	{"select_query", SelectQuery, METH_VARARGS, "execute select query"},
	{"delete_query", DeleteQuery, METH_VARARGS, "execute delete query"},
	{"update_query", UpdateQuery, METH_VARARGS, "execute update query"},
	{"set_object", SetObject, METH_VARARGS, "add update query"},
	{"set", Set, METH_VARARGS, "add field update"},
	{"drop", Drop, METH_VARARGS, "drop values"},
	{"expression", SetExpression, METH_VARARGS, "set expression"},
	{"join", Join, METH_VARARGS, "join 2 query"},
	{"merge", Merge, METH_VARARGS, "merge 2 query"},
	{"on", On, METH_VARARGS, "on specifies join condition"},
	{"select_filter", SelectFilter, METH_VARARGS, "select add filter to fields of result's objects"},
	{"functions", AddFunctions, METH_VARARGS, "add sql-functions to query"},
	{"equal_position", AddEqualPosition, METH_VARARGS, "add equal position fields"},

	{nullptr, nullptr, 0, nullptr}
};
// clang-format on

static struct PyModuleDef module_definition = {
	PyModuleDef_HEAD_INIT, MODULE_NAME, MODULE_DESCRIPTION, -1, module_methods, nullptr, nullptr, nullptr, nullptr};

PyMODINIT_FUNC MODULE_EXPORT_FUNCTION(void) {
	Py_Initialize();
	return PyModule_Create(&module_definition);
}

}  // namespace pyreindexer

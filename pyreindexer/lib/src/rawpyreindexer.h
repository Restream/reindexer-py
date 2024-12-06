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

static PyObject* Init(PyObject* self, PyObject* args);
static PyObject* Destroy(PyObject* self, PyObject* args);
static PyObject* Connect(PyObject* self, PyObject* args);
static PyObject* NamespaceOpen(PyObject* self, PyObject* args);
static PyObject* NamespaceClose(PyObject* self, PyObject* args);
static PyObject* NamespaceDrop(PyObject* self, PyObject* args);
static PyObject* IndexAdd(PyObject* self, PyObject* args);
static PyObject* IndexUpdate(PyObject* self, PyObject* args);
static PyObject* IndexDrop(PyObject* self, PyObject* args);
static PyObject* ItemInsert(PyObject* self, PyObject* args);
static PyObject* ItemUpdate(PyObject* self, PyObject* args);
static PyObject* ItemUpsert(PyObject* self, PyObject* args);
static PyObject* ItemDelete(PyObject* self, PyObject* args);
static PyObject* PutMeta(PyObject* self, PyObject* args);
static PyObject* GetMeta(PyObject* self, PyObject* args);
static PyObject* DeleteMeta(PyObject* self, PyObject* args);
static PyObject* Select(PyObject* self, PyObject* args);
static PyObject* EnumMeta(PyObject* self, PyObject* args);
static PyObject* EnumNamespaces(PyObject* self, PyObject* args);

static PyObject* QueryResultsWrapperIterate(PyObject* self, PyObject* args);
static PyObject* QueryResultsWrapperDelete(PyObject* self, PyObject* args);
static PyObject* GetAggregationResults(PyObject* self, PyObject* args);

static PyObject* NewTransaction(PyObject* self, PyObject* args);
static PyObject* ItemInsertTransaction(PyObject* self, PyObject* args);
static PyObject* ItemUpdateTransaction(PyObject* self, PyObject* args);
static PyObject* ItemUpsertTransaction(PyObject* self, PyObject* args);
static PyObject* ItemDeleteTransaction(PyObject* self, PyObject* args);
static PyObject* CommitTransaction(PyObject* self, PyObject* args);
static PyObject* RollbackTransaction(PyObject* self, PyObject* args);

// clang-format off
static PyMethodDef module_methods[] = {
	{"init", Init, METH_NOARGS, "init reindexer instance"},
	{"destroy", Destroy, METH_VARARGS, "destroy reindexer instance"},
	{"connect", Connect, METH_VARARGS, "connect to reindexer database"},
	{"namespace_open", NamespaceOpen, METH_VARARGS, "open namespace"},
	{"namespace_close", NamespaceClose, METH_VARARGS, "close namespace"},
	{"namespace_drop", NamespaceDrop, METH_VARARGS, "drop namespace"},
	{"namespaces_enum", EnumNamespaces, METH_VARARGS, "enum namespaces"},
	{"index_add", IndexAdd, METH_VARARGS, "add index"},
	{"index_update", IndexUpdate, METH_VARARGS, "update index"},
	{"index_drop", IndexDrop, METH_VARARGS, "drop index"},
	{"item_insert", ItemInsert, METH_VARARGS, "insert item"},
	{"item_update", ItemUpdate, METH_VARARGS, "update item"},
	{"item_upsert", ItemUpsert, METH_VARARGS, "upsert item"},
	{"item_delete", ItemDelete, METH_VARARGS, "delete item"},
	{"meta_put", PutMeta, METH_VARARGS, "put meta"},
	{"meta_get", GetMeta, METH_VARARGS, "get meta"},
	{"meta_delete", DeleteMeta, METH_VARARGS, "delete meta"},
	{"meta_enum", EnumMeta, METH_VARARGS, "enum meta"},
	{"select", Select, METH_VARARGS, "select query"},

	{"query_results_iterate", QueryResultsWrapperIterate, METH_VARARGS, "get query result"},
	{"query_results_delete", QueryResultsWrapperDelete, METH_VARARGS, "free query results buffer"},
	{"get_agg_results", GetAggregationResults, METH_VARARGS, "get aggregation results"},

	{"new_transaction", NewTransaction, METH_VARARGS, "start new transaction"},
	{"item_insert_transaction", ItemInsertTransaction, METH_VARARGS, "item insert transaction"},
	{"item_update_transaction", ItemUpdateTransaction, METH_VARARGS, "item update transaction"},
	{"item_upsert_transaction", ItemUpsertTransaction, METH_VARARGS, "item upsert transaction"},
	{"item_delete_transaction", ItemDeleteTransaction, METH_VARARGS, "item delete transaction"},
	{"commit_transaction", CommitTransaction, METH_VARARGS, "apply changes. Free transaction object memory"},
	{"rollback_transaction", RollbackTransaction, METH_VARARGS, "rollback changes. Free transaction object memory"},

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

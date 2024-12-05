#include "rawpyreindexer.h"

#include "pyobjtools.h"
#include "queryresults_wrapper.h"
#include "transaction_wrapper.h"
#include "tools/serializer.h"

namespace pyreindexer {

using reindexer::Error;
using reindexer::IndexDef;
using reindexer::NamespaceDef;
using reindexer::WrSerializer;

static uintptr_t initReindexer() {
	DBInterface* db = new DBInterface();
	return reinterpret_cast<uintptr_t>(db);
}

static DBInterface* getDB(uintptr_t rx) { return reinterpret_cast<DBInterface*>(rx); }

static void destroyReindexer(uintptr_t rx) {
	DBInterface* db = getDB(rx);
	delete db;
}

static PyObject* pyErr(const Error& err) { return Py_BuildValue("is", err.code(), err.what().c_str()); }

template <typename T>
static T* getWrapper(uintptr_t wrapperAddr) {
	return reinterpret_cast<T*>(wrapperAddr);
}

template <typename T>
static void wrapperDelete(uintptr_t wrapperAddr) {
	T* queryWrapperPtr = getWrapper<T>(wrapperAddr);
	delete queryWrapperPtr;
}

static PyObject* queryResultsWrapperIterate(uintptr_t qresWrapperAddr) {
	QueryResultsWrapper* qresWrapperPtr = getWrapper<QueryResultsWrapper>(qresWrapperAddr);

	WrSerializer wrSer;
	qresWrapperPtr->GetItemJSON(wrSer, false);
	qresWrapperPtr->Next();

	PyObject* dictFromJson = nullptr;
	try {
		dictFromJson = PyObjectFromJson(reindexer::giftStr(wrSer.Slice()));  // stolen ref
	} catch (const Error& err) {
		Py_XDECREF(dictFromJson);

		return Py_BuildValue("is{}", err.code(), err.what().c_str());
	}

	PyObject* res = Py_BuildValue("isO", errOK, "", dictFromJson);  // new ref
	Py_DECREF(dictFromJson);

	return res;
}

static PyObject* Init(PyObject* self, PyObject* args) {
	uintptr_t rx = initReindexer();
	if (rx == 0) {
		PyErr_SetString(PyExc_RuntimeError, "Initialization error");

		return nullptr;
	}

	return Py_BuildValue("k", rx);
}

static PyObject* Destroy(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	if (!PyArg_ParseTuple(args, "k", &rx)) {
		return nullptr;
	}

	destroyReindexer(rx);

	Py_RETURN_NONE;
}

static PyObject* Connect(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* dsn = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &rx, &dsn)) {
		return nullptr;
	}

	Error err = getDB(rx)->Connect(dsn);
	return pyErr(err);
}

static PyObject* NamespaceOpen(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &rx, &ns)) {
		return nullptr;
	}

	Error err = getDB(rx)->OpenNamespace(ns);
	return pyErr(err);
}

static PyObject* NamespaceClose(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &rx, &ns)) {
		return nullptr;
	}

	Error err = getDB(rx)->CloseNamespace(ns);
	return pyErr(err);
}

static PyObject* NamespaceDrop(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &rx, &ns)) {
		return nullptr;
	}

	Error err = getDB(rx)->DropNamespace(ns);
	return pyErr(err);
}

static PyObject* IndexAdd(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	PyObject* indexDefDict = nullptr;  // borrowed ref after ParseTuple
	if (!PyArg_ParseTuple(args, "ksO!", &rx, &ns, &PyDict_Type, &indexDefDict)) {
		return nullptr;
	}

	Py_INCREF(indexDefDict);

	WrSerializer wrSer;

	try {
		PyObjectToJson(&indexDefDict, wrSer);
	} catch (const Error& err) {
		Py_DECREF(indexDefDict);

		return pyErr(err);
	}

	Py_DECREF(indexDefDict);

	IndexDef indexDef;
	Error err = indexDef.FromJSON(reindexer::giftStr(wrSer.Slice()));
	if (err.ok()) {
		err = getDB(rx)->AddIndex(ns, indexDef);
	}
	return pyErr(err);
}

static PyObject* IndexUpdate(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	PyObject* indexDefDict = nullptr;  // borrowed ref after ParseTuple
	if (!PyArg_ParseTuple(args, "ksO!", &rx, &ns, &PyDict_Type, &indexDefDict)) {
		return nullptr;
	}

	Py_INCREF(indexDefDict);

	WrSerializer wrSer;

	try {
		PyObjectToJson(&indexDefDict, wrSer);
	} catch (const Error& err) {
		Py_DECREF(indexDefDict);

		return pyErr(err);
	}

	Py_DECREF(indexDefDict);

	IndexDef indexDef;
	Error err = indexDef.FromJSON(reindexer::giftStr(wrSer.Slice()));
	if (err.ok()) {
		err = getDB(rx)->UpdateIndex(ns, indexDef);
	}
	return pyErr(err);
}

static PyObject* IndexDrop(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char *ns = nullptr, *indexName = nullptr;
	if (!PyArg_ParseTuple(args, "kss", &rx, &ns, &indexName)) {
		return nullptr;
	}

	Error err = getDB(rx)->DropIndex(ns, IndexDef(indexName));
	return pyErr(err);
}

static PyObject* itemModify(PyObject* self, PyObject* args, ItemModifyMode mode) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	PyObject* itemDefDict = nullptr;  	// borrowed ref after ParseTuple
	PyObject* preceptsList = nullptr;  	// borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "ksO!|O!", &rx, &ns, &PyDict_Type, &itemDefDict, &PyList_Type, &preceptsList)) {
		return nullptr;
	}

	Py_INCREF(itemDefDict);
	Py_XINCREF(preceptsList);

	auto item = getDB(rx)->NewItem(ns);
	Error err = item.Status();
	if (!err.ok()) {
		return pyErr(err);
	}

	WrSerializer wrSer;

	try {
		PyObjectToJson(&itemDefDict, wrSer);
	} catch (const Error& err) {
		Py_DECREF(itemDefDict);
		Py_XDECREF(preceptsList);

		return pyErr(err);
	}

	Py_DECREF(itemDefDict);

	err = item.Unsafe().FromJSON(wrSer.c_str(), 0, mode == ModeDelete);
	if (!err.ok()) {
		Py_XDECREF(preceptsList);

		return pyErr(err);
	}

	if (preceptsList != nullptr && mode != ModeDelete) {
		std::vector<std::string> itemPrecepts;

		try {
			itemPrecepts = ParseListToStrVec(&preceptsList);
		} catch (const Error& err) {
			Py_DECREF(preceptsList);

			return pyErr(err);
		}

		item.SetPrecepts(itemPrecepts); // ToDo after migrate on v.4, do std::move
	}

	Py_XDECREF(preceptsList);

	switch (mode) {
		case ModeInsert:
			err = getDB(rx)->Insert(ns, item);
			break;
		case ModeUpdate:
			err = getDB(rx)->Update(ns, item);
			break;
		case ModeUpsert:
			err = getDB(rx)->Upsert(ns, item);
			break;
		case ModeDelete:
			err = getDB(rx)->Delete(ns, item);
			break;
		default:
			PyErr_SetString(PyExc_RuntimeError, "Unknown item modify mode");
			return nullptr;
	}

	return pyErr(err);
}

static PyObject* ItemInsert(PyObject* self, PyObject* args) { return itemModify(self, args, ModeInsert); }
static PyObject* ItemUpdate(PyObject* self, PyObject* args) { return itemModify(self, args, ModeUpdate); }
static PyObject* ItemUpsert(PyObject* self, PyObject* args) { return itemModify(self, args, ModeUpsert); }
static PyObject* ItemDelete(PyObject* self, PyObject* args) { return itemModify(self, args, ModeDelete); }

static PyObject* PutMeta(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char *ns = nullptr, *key = nullptr, *value = nullptr;
	if (!PyArg_ParseTuple(args, "ksss", &rx, &ns, &key, &value)) {
		return nullptr;
	}

	Error err = getDB(rx)->PutMeta(ns, key, value);
	return pyErr(err);
}

static PyObject* GetMeta(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char *ns = nullptr, *key = nullptr;
	if (!PyArg_ParseTuple(args, "kss", &rx, &ns, &key)) {
		return nullptr;
	}

	std::string value;
	Error err = getDB(rx)->GetMeta(ns, key, value);
	return Py_BuildValue("iss", err.code(), err.what().c_str(), value.c_str());
}

static PyObject* DeleteMeta(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char *ns = nullptr, *key = nullptr;
	if (!PyArg_ParseTuple(args, "kss", &rx, &ns, &key)) {
		return nullptr;
	}

	Error err = getDB(rx)->DeleteMeta(ns, key);
	return pyErr(err);
}

static PyObject* Select(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* query = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &rx, &query)) {
		return nullptr;
	}

	auto db = getDB(rx);
	auto qresWrapper = new QueryResultsWrapper(db);
	Error err = qresWrapper->Select(query);

	if (!err.ok()) {
		delete qresWrapper;

		return Py_BuildValue("iskI", err.code(), err.what().c_str(), 0, 0);
	}

	return Py_BuildValue("iskI", err.code(), err.what().c_str(), reinterpret_cast<uintptr_t>(qresWrapper), qresWrapper->Count());
}

static PyObject* EnumMeta(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &rx, &ns)) {
		return nullptr;
	}

	std::vector<std::string> keys;
	Error err = getDB(rx)->EnumMeta(ns, keys);
	if (!err.ok()) {
		return Py_BuildValue("is[]", err.code(), err.what().c_str());
	}

	PyObject* list = PyList_New(keys.size());  // new ref
	if (!list) {
		return nullptr;
	}

	Py_ssize_t pos = 0;
	for (const auto& key : keys) {
		PyObject* pyKey = PyUnicode_FromStringAndSize(key.data(), key.size());  // new ref
		PyList_SetItem(list, pos, pyKey);  // stolen ref
		++pos;
	}

	PyObject* res = Py_BuildValue("isO", err.code(), err.what().c_str(), list);
	Py_DECREF(list);

	return res;
}

static PyObject* EnumNamespaces(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	unsigned enumAll = 0;
	if (!PyArg_ParseTuple(args, "kI", &rx, &enumAll)) {
		return nullptr;
	}

	std::vector<NamespaceDef> nsDefs;
	Error err = getDB(rx)->EnumNamespaces(nsDefs, reindexer::EnumNamespacesOpts().WithClosed(enumAll));
	if (!err.ok()) {
		return Py_BuildValue("is[]", err.code(), err.what().c_str());
	}

	PyObject* list = PyList_New(nsDefs.size());	 // new ref
	if (!list) {
		return nullptr;
	}

	WrSerializer wrSer;
	Py_ssize_t pos = 0;
	for (const auto& ns : nsDefs) {
		wrSer.Reset();
		ns.GetJSON(wrSer, false);

		PyObject* dictFromJson = nullptr;
		try {
			dictFromJson = PyObjectFromJson(reindexer::giftStr(wrSer.Slice()));  // stolen ref
		} catch (const Error& err) {
			Py_XDECREF(dictFromJson);
			Py_DECREF(list);

			return Py_BuildValue("is{}", err.code(), err.what().c_str());
		}

		PyList_SetItem(list, pos, dictFromJson);  // stolen ref
		++pos;
	}

	PyObject* res = Py_BuildValue("isO", err.code(), err.what().c_str(), list);
	Py_DECREF(list);

	return res;
}

static PyObject* QueryResultsWrapperIterate(PyObject* self, PyObject* args) {
	uintptr_t qresWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &qresWrapperAddr)) {
		return nullptr;
	}

	return queryResultsWrapperIterate(qresWrapperAddr);
}

static PyObject* QueryResultsWrapperDelete(PyObject* self, PyObject* args) {
	uintptr_t qresWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &qresWrapperAddr)) {
		return nullptr;
	}

	wrapperDelete<QueryResultsWrapper>(qresWrapperAddr);

	Py_RETURN_NONE;
}

static PyObject* GetAggregationResults(PyObject* self, PyObject* args) {
	uintptr_t qresWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &qresWrapperAddr)) {
		return nullptr;
	}

	QueryResultsWrapper* qresWrapper = getWrapper<QueryResultsWrapper>(qresWrapperAddr);

	const auto& aggResults = qresWrapper->GetAggregationResults();
	WrSerializer wrSer;
	wrSer << "[";
	for (size_t i = 0; i < aggResults.size(); ++i) {
		if (i > 0) {
			wrSer << ',';
		}

		aggResults[i].GetJSON(wrSer);
	}
	wrSer << "]";

	PyObject* dictFromJson = nullptr;
	try {
		dictFromJson = PyObjectFromJson(reindexer::giftStr(wrSer.Slice()));  // stolen ref
	} catch (const Error& err) {
		Py_XDECREF(dictFromJson);

		return Py_BuildValue("is{}", err.code(), err.what().c_str());
	}

	PyObject* res = Py_BuildValue("isO", errOK, "", dictFromJson);  // new ref
	Py_DECREF(dictFromJson);

	return res;
}

static PyObject* NewTransaction(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &rx, &ns)) {
		return nullptr;
	}

	auto db = getDB(rx);
	auto transaction = new TransactionWrapper(db);
	Error err =  transaction->Start(ns);
	if (!err.ok()) {
		delete transaction;

		return Py_BuildValue("isk", err.code(), err.what().c_str(), 0);
	}

	return Py_BuildValue("isk", err.code(), err.what().c_str(), reinterpret_cast<uintptr_t>(transaction));
}

static PyObject* itemModifyTransaction(PyObject* self, PyObject* args, ItemModifyMode mode) {
	uintptr_t transactionWrapperAddr = 0;
	PyObject* itemDefDict = nullptr;  	// borrowed ref after ParseTuple
	PyObject* preceptsList = nullptr;  	// borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "kO!|O!", &transactionWrapperAddr, &PyDict_Type, &itemDefDict, &PyList_Type, &preceptsList)) {
		return nullptr;
	}

	Py_INCREF(itemDefDict);
	Py_XINCREF(preceptsList);

	auto transaction = getWrapper<TransactionWrapper>(transactionWrapperAddr);

	auto item = transaction->NewItem();
	Error err = item.Status();
	if (!err.ok()) {
		Py_DECREF(itemDefDict);
		Py_XDECREF(preceptsList);

		return pyErr(err);
	}

	WrSerializer wrSer;

	try {
		PyObjectToJson(&itemDefDict, wrSer);
	} catch (const Error& err) {
		Py_DECREF(itemDefDict);
		Py_XDECREF(preceptsList);

		return pyErr(err);
	}

	Py_DECREF(itemDefDict);

	err = item.Unsafe().FromJSON(wrSer.c_str(), 0, mode == ModeDelete);
	if (!err.ok()) {
		Py_XDECREF(preceptsList);

		return pyErr(err);
	}

	if (preceptsList != nullptr && mode != ModeDelete) {
		std::vector<std::string> itemPrecepts;

		try {
			itemPrecepts = ParseListToStrVec(&preceptsList);
		} catch (const Error& err) {
			Py_DECREF(preceptsList);

			return pyErr(err);
		}

		item.SetPrecepts(itemPrecepts); // ToDo after migrate on v.4, do std::move
	}

	Py_XDECREF(preceptsList);

	switch (mode) {
		case ModeInsert:
		case ModeUpdate:
		case ModeUpsert:
		case ModeDelete:
			err = transaction->Modify(std::move(item), mode);
			return pyErr(err);
		default:
			PyErr_SetString(PyExc_RuntimeError, "Unknown item modify transaction mode");
			return nullptr;
	}

	return nullptr;
}
static PyObject* ItemInsertTransaction(PyObject* self, PyObject* args) { return itemModifyTransaction(self, args, ModeInsert); }
static PyObject* ItemUpdateTransaction(PyObject* self, PyObject* args) { return itemModifyTransaction(self, args, ModeUpdate); }
static PyObject* ItemUpsertTransaction(PyObject* self, PyObject* args) { return itemModifyTransaction(self, args, ModeUpsert); }
static PyObject* ItemDeleteTransaction(PyObject* self, PyObject* args) { return itemModifyTransaction(self, args, ModeDelete); }

static PyObject* CommitTransaction(PyObject* self, PyObject* args) {
	uintptr_t transactionWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &transactionWrapperAddr)) {
		return nullptr;
	}

	auto transaction = getWrapper<TransactionWrapper>(transactionWrapperAddr);

	size_t count = 0;
	Error err = transaction->Commit(count);

	wrapperDelete<TransactionWrapper>(transactionWrapperAddr);

	return Py_BuildValue("isI", err.code(), err.what().c_str(), count);
}

static PyObject* RollbackTransaction(PyObject* self, PyObject* args) {
	uintptr_t transactionWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &transactionWrapperAddr)) {
		return nullptr;
	}

	auto transaction = getWrapper<TransactionWrapper>(transactionWrapperAddr);

	Error err = transaction->Rollback();

	wrapperDelete<TransactionWrapper>(transactionWrapperAddr);

	return pyErr(err);
}

}  // namespace pyreindexer

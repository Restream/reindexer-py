#include "rawpyreindexer.h"

#include "pyobjtools.h"
#include "queryresults_wrapper.h"
#include "query_wrapper.h"
#include "transaction_wrapper.h"
#include "tools/serializer.h"

namespace pyreindexer {

using reindexer::Error;
using reindexer::IndexDef;
using reindexer::NamespaceDef;
using reindexer::WrSerializer;

namespace {
uintptr_t initReindexer() {
	DBInterface* db = new DBInterface();
	return reinterpret_cast<uintptr_t>(db);
}

DBInterface* getDB(uintptr_t rx) { return reinterpret_cast<DBInterface*>(rx); }

void destroyReindexer(uintptr_t rx) {
	DBInterface* db = getDB(rx);
	delete db;
}

PyObject* pyErr(const Error& err) { return Py_BuildValue("is", err.code(), err.what().c_str()); }

template <typename T>
T* getWrapper(uintptr_t wrapperAddr) {
	return reinterpret_cast<T*>(wrapperAddr);
}

template <typename T>
void wrapperDelete(uintptr_t wrapperAddr) {
	T* queryWrapperPtr = getWrapper<T>(wrapperAddr);
	delete queryWrapperPtr;
}

PyObject* queryResultsWrapperIterate(uintptr_t qresWrapperAddr) {
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
} // namespace

// common --------------------------------------------------------------------------------------------------------------

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

	auto err = getDB(rx)->Connect(dsn);
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
	auto err = qresWrapper->Select(query);

	if (!err.ok()) {
		delete qresWrapper;

		return Py_BuildValue("iskI", err.code(), err.what().c_str(), 0, 0);
	}

	return Py_BuildValue("iskI", err.code(), err.what().c_str(), reinterpret_cast<uintptr_t>(qresWrapper), qresWrapper->Count());
}

// namespace ----------------------------------------------------------------------------------------------------------

static PyObject* NamespaceOpen(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &rx, &ns)) {
		return nullptr;
	}

	auto err = getDB(rx)->OpenNamespace(ns);
	return pyErr(err);
}

static PyObject* NamespaceClose(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &rx, &ns)) {
		return nullptr;
	}

	auto err = getDB(rx)->CloseNamespace(ns);
	return pyErr(err);
}

static PyObject* NamespaceDrop(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &rx, &ns)) {
		return nullptr;
	}

	auto err = getDB(rx)->DropNamespace(ns);
	return pyErr(err);
}

static PyObject* EnumNamespaces(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	unsigned enumAll = 0;
	if (!PyArg_ParseTuple(args, "kI", &rx, &enumAll)) {
		return nullptr;
	}

	std::vector<NamespaceDef> nsDefs;
	auto err = getDB(rx)->EnumNamespaces(nsDefs, reindexer::EnumNamespacesOpts().WithClosed(enumAll));
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

// index ---------------------------------------------------------------------------------------------------------------

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
	auto err = indexDef.FromJSON(reindexer::giftStr(wrSer.Slice()));
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
	auto err = indexDef.FromJSON(reindexer::giftStr(wrSer.Slice()));
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

	auto err = getDB(rx)->DropIndex(ns, IndexDef(indexName));
	return pyErr(err);
}

// item ----------------------------------------------------------------------------------------------------------------

namespace {
PyObject* itemModify(PyObject* self, PyObject* args, ItemModifyMode mode) {
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
	auto err = item.Status();
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

	char* json = const_cast<char*>(wrSer.c_str());
	err = item.Unsafe().FromJSON(json, 0, mode == ModeDelete);
	if (!err.ok()) {
		Py_XDECREF(preceptsList);

		return pyErr(err);
	}

	if (preceptsList != nullptr && mode != ModeDelete) {
		std::vector<std::string> itemPrecepts;

		try {
			itemPrecepts = ParseStrListToStrVec(&preceptsList);
		} catch (const Error& err) {
			Py_DECREF(preceptsList);

			return pyErr(err);
		}

		item.SetPrecepts(itemPrecepts);
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
} // namespace
static PyObject* ItemInsert(PyObject* self, PyObject* args) { return itemModify(self, args, ModeInsert); }
static PyObject* ItemUpdate(PyObject* self, PyObject* args) { return itemModify(self, args, ModeUpdate); }
static PyObject* ItemUpsert(PyObject* self, PyObject* args) { return itemModify(self, args, ModeUpsert); }
static PyObject* ItemDelete(PyObject* self, PyObject* args) { return itemModify(self, args, ModeDelete); }

// meta ----------------------------------------------------------------------------------------------------------------

static PyObject* PutMeta(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char *ns = nullptr, *key = nullptr, *value = nullptr;
	if (!PyArg_ParseTuple(args, "ksss", &rx, &ns, &key, &value)) {
		return nullptr;
	}

	auto err = getDB(rx)->PutMeta(ns, key, value);
	return pyErr(err);
}

static PyObject* GetMeta(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char *ns = nullptr, *key = nullptr;
	if (!PyArg_ParseTuple(args, "kss", &rx, &ns, &key)) {
		return nullptr;
	}

	std::string value;
	auto err = getDB(rx)->GetMeta(ns, key, value);
	return Py_BuildValue("iss", err.code(), err.what().c_str(), value.c_str());
}

static PyObject* DeleteMeta(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char *ns = nullptr, *key = nullptr;
	if (!PyArg_ParseTuple(args, "kss", &rx, &ns, &key)) {
		return nullptr;
	}

	auto err = getDB(rx)->DeleteMeta(ns, key);
	return pyErr(err);
}

static PyObject* EnumMeta(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &rx, &ns)) {
		return nullptr;
	}

	std::vector<std::string> keys;
	auto err = getDB(rx)->EnumMeta(ns, keys);
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

// query results -------------------------------------------------------------------------------------------------------

static PyObject* QueryResultsWrapperStatus(PyObject* self, PyObject* args) {
	uintptr_t qresWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &qresWrapperAddr)) {
		return nullptr;
	}

	QueryResultsWrapper* qresWrapper = getWrapper<QueryResultsWrapper>(qresWrapperAddr);
	auto err = qresWrapper->Status();
	return pyErr(err);
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

static PyObject* GetExplainResults(PyObject* self, PyObject* args) {
	uintptr_t qresWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &qresWrapperAddr)) {
		return nullptr;
	}

	QueryResultsWrapper* qresWrapper = getWrapper<QueryResultsWrapper>(qresWrapperAddr);

	const auto& explainResults = qresWrapper->GetExplainResults();

	return Py_BuildValue("iss", errOK, "", explainResults.c_str());
}

// transaction ---------------------------------------------------------------------------------------------------------

static PyObject* NewTransaction(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &rx, &ns)) {
		return nullptr;
	}

	auto db = getDB(rx);
	auto transaction = new TransactionWrapper(db);
	auto err = transaction->Start(ns);
	if (!err.ok()) {
		delete transaction;

		return Py_BuildValue("isk", err.code(), err.what().c_str(), 0);
	}

	return Py_BuildValue("isk", err.code(), err.what().c_str(), reinterpret_cast<uintptr_t>(transaction));
}

namespace {
PyObject* itemModifyTransaction(PyObject* self, PyObject* args, ItemModifyMode mode) {
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
	auto err = item.Status();
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

	char* json = const_cast<char*>(wrSer.c_str());
	err = item.Unsafe().FromJSON(json, 0, mode == ModeDelete);
	if (!err.ok()) {
		Py_XDECREF(preceptsList);

		return pyErr(err);
	}

	if (preceptsList != nullptr && mode != ModeDelete) {
		std::vector<std::string> itemPrecepts;

		try {
			itemPrecepts = ParseStrListToStrVec(&preceptsList);
		} catch (const Error& err) {
			Py_DECREF(preceptsList);

			return pyErr(err);
		}

		item.SetPrecepts(itemPrecepts);
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
} // namespace
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

	assert((StopTransactionMode::Commit == stopMode) || (StopTransactionMode::Rollback == stopMode));
	size_t count = 0;
	auto err = transaction->Commit(count);

	wrapperDelete<TransactionWrapper>(transactionWrapperAddr);

	return Py_BuildValue("isI", err.code(), err.what().c_str(), count);
}

static PyObject* RollbackTransaction(PyObject* self, PyObject* args) {
	uintptr_t transactionWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &transactionWrapperAddr)) {
		return nullptr;
	}

	auto transaction = getWrapper<TransactionWrapper>(transactionWrapperAddr);

	assert((StopTransactionMode::Commit == stopMode) || (StopTransactionMode::Rollback == stopMode));
	auto err = transaction->Rollback();

	wrapperDelete<TransactionWrapper>(transactionWrapperAddr);

	return pyErr(err);
}

// query ---------------------------------------------------------------------------------------------------------------

static PyObject* CreateQuery(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &rx, &ns)) {
		return nullptr;
	}

	auto db = getDB(rx);
	auto query = new QueryWrapper(db, ns);
	return Py_BuildValue("isK", errOK, "", reinterpret_cast<uintptr_t>(query));
}

static PyObject* DestroyQuery(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &queryWrapperAddr)) {
		return nullptr;
	}

	wrapperDelete<QueryWrapper>(queryWrapperAddr);

	Py_RETURN_NONE;
}

static PyObject* Where(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* index = nullptr;
	unsigned condition = 0;
	PyObject* keysList = nullptr;  	// borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "ksIO!", &queryWrapperAddr, &index, &condition, &PyList_Type, &keysList)) {
		return nullptr;
	}

	Py_XINCREF(keysList);

	std::vector<reindexer::Variant> keys;
	if (keysList != nullptr) {
		try {
			keys = ParseListToVec(&keysList);
		} catch (const Error& err) {
			Py_DECREF(keysList);

			return pyErr(err);
		}
	}

	Py_XDECREF(keysList);

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->Where(index, CondType(condition), keys);

	return pyErr(errOK);
}

static PyObject* WhereQuery(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	uintptr_t subQueryWrapperAddr = 0;
	unsigned condition = 0;
	PyObject* keysList = nullptr;  	// borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "kkIO!", &queryWrapperAddr, &subQueryWrapperAddr, &condition, &PyList_Type, &keysList)) {
		return nullptr;
	}

	Py_XINCREF(keysList);

	std::vector<reindexer::Variant> keys;
	if (keysList != nullptr) {
		try {
			keys = ParseListToVec(&keysList);
		} catch (const Error& err) {
			Py_DECREF(keysList);

			return pyErr(err);
		}
	}

	Py_XDECREF(keysList);

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);
	auto subQuery = getWrapper<QueryWrapper>(subQueryWrapperAddr);

	query->WhereQuery(*subQuery, CondType(condition), keys);

	return pyErr(errOK);
}

static PyObject* WhereComposite(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* index = nullptr;
	unsigned condition = 0;
	uintptr_t subQueryWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "ksIk", &queryWrapperAddr, &index, &condition, &subQueryWrapperAddr)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);
	auto subQuery = getWrapper<QueryWrapper>(subQueryWrapperAddr);

	query->WhereComposite(index, CondType(condition), *subQuery);

	Py_RETURN_NONE;
}

static PyObject* WhereUUID(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* index = nullptr;
	unsigned condition = 0;
	PyObject* keysList = nullptr;  	// borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "ksIO!", &queryWrapperAddr, &index, &condition, &PyList_Type, &keysList)) {
		return nullptr;
	}

	Py_XINCREF(keysList);

	std::vector<std::string> keys;
	if (keysList != nullptr) {
		try {
			keys = ParseStrListToStrVec(&keysList);
		} catch (const Error& err) {
			Py_DECREF(keysList);

			return pyErr(err);
		}
	}

	Py_XDECREF(keysList);

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->WhereUUID(index, CondType(condition), keys);

	return pyErr(errOK);
}

static PyObject* WhereBetweenFields(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* first_field = nullptr;
	unsigned condition = 0;
	char* second_field = nullptr;
	if (!PyArg_ParseTuple(args, "ksIs", &queryWrapperAddr, &first_field, &condition, &second_field)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->WhereBetweenFields(first_field, CondType(condition), second_field);

	Py_RETURN_NONE;
}

namespace {
enum class BracketType { Open, Closed };
PyObject* addBracket(PyObject* self, PyObject* args, BracketType type) {
	uintptr_t queryWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &queryWrapperAddr)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	auto err = (type == BracketType::Open)? query->OpenBracket() : query->CloseBracket();
	return pyErr(err);
}
} // namespace
static PyObject* OpenBracket(PyObject* self, PyObject* args) { return addBracket(self, args, BracketType::Open); }
static PyObject* CloseBracket(PyObject* self, PyObject* args) { return addBracket(self, args, BracketType::Closed); }

static PyObject* DWithin(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* index = nullptr;
	double x = 0, y = 0, distance = 0;
	if (!PyArg_ParseTuple(args, "ksddd", &queryWrapperAddr, &index, &x, &y, &distance)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->DWithin(index, x, y, distance);

	Py_RETURN_NONE;
}

namespace {
PyObject* aggregate(PyObject* self, PyObject* args, AggType type) {
	uintptr_t queryWrapperAddr = 0;
	char* field = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &queryWrapperAddr, &field)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->Aggregate(field, type);

	Py_RETURN_NONE;
}
} // namespace
static PyObject* AggregateDistinct(PyObject* self, PyObject* args) { return aggregate(self, args, AggType::AggDistinct); }
static PyObject* AggregateSum(PyObject* self, PyObject* args) { return aggregate(self, args, AggType::AggSum); }
static PyObject* AggregateAvg(PyObject* self, PyObject* args) { return aggregate(self, args, AggType::AggAvg); }
static PyObject* AggregateMin(PyObject* self, PyObject* args) { return aggregate(self, args, AggType::AggMin); }
static PyObject* AggregateMax(PyObject* self, PyObject* args) { return aggregate(self, args, AggType::AggMax); }

namespace {
static PyObject* addValue(PyObject* self, PyObject* args, QueryItemType type) {
	uintptr_t queryWrapperAddr = 0;
	int value = 0;
	if (!PyArg_ParseTuple(args, "ki", &queryWrapperAddr, &value)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->AddValue(type, value);

	Py_RETURN_NONE;
}
} // namespace
static PyObject* AggregationLimit(PyObject* self, PyObject* args) { return addValue(self, args, QueryItemType::QueryAggregationLimit); }
static PyObject* AggregationOffset(PyObject* self, PyObject* args) { return addValue(self, args, QueryItemType::QueryAggregationOffset); }

static PyObject* AggregationSort(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* field = nullptr;
	unsigned desc = 0;
	if (!PyArg_ParseTuple(args, "ksI", &queryWrapperAddr, &field, &desc)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->AggregationSort(field, (desc != 0));

	return pyErr(errOK);
}

static PyObject* Aggregation(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	PyObject* fieldsList = nullptr;  	// borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "kO!", &queryWrapperAddr, &PyList_Type, &fieldsList)) {
		return nullptr;
	}

	Py_XINCREF(fieldsList);

	std::vector<std::string> fields;
	if (fieldsList != nullptr) {
		try {
			fields = ParseStrListToStrVec(&fieldsList);
		} catch (const Error& err) {
			Py_DECREF(fieldsList);

			return pyErr(err);
		}
	}

	Py_XDECREF(fieldsList);

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->Aggregation(fields);

	return pyErr(errOK);
}

static PyObject* Sort(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* index = nullptr;
	unsigned desc = 0;
	PyObject* keysList = nullptr;  	// borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "ksIO!", &queryWrapperAddr, &index, &desc, &PyList_Type, &keysList)) {
		return nullptr;
	}

	Py_XINCREF(keysList);

	std::vector<reindexer::Variant> keys;
	if (keysList != nullptr) {
		try {
			keys = ParseListToVec(&keysList);
		} catch (const Error& err) {
			Py_DECREF(keysList);

			return pyErr(err);
		}
	}

	Py_XDECREF(keysList);

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->Sort(index, (desc != 0), keys);

	return pyErr(errOK);
}

namespace {
PyObject* logOp(PyObject* self, PyObject* args, OpType opID) {
	uintptr_t queryWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &queryWrapperAddr)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->LogOp(opID);

	Py_RETURN_NONE;
}
} // namespace
static PyObject* And(PyObject* self, PyObject* args) { return logOp(self, args, OpType::OpAnd); }
static PyObject* Or(PyObject* self, PyObject* args) { return logOp(self, args, OpType::OpOr); }
static PyObject* Not(PyObject* self, PyObject* args) { return logOp(self, args, OpType::OpNot); }

namespace {
static PyObject* total(PyObject* self, PyObject* args, CalcTotalMode mode) {
	uintptr_t queryWrapperAddr = 0;
	char* totalName = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &queryWrapperAddr, &totalName)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->Total(totalName, mode);

	Py_RETURN_NONE;
}
} // namespace
static PyObject* ReqTotal(PyObject* self, PyObject* args) { return total(self, args, CalcTotalMode::ModeAccurateTotal); }
static PyObject* CachedTotal(PyObject* self, PyObject* args) { return total(self, args, CalcTotalMode::ModeCachedTotal); }

static PyObject* Limit(PyObject* self, PyObject* args) { return addValue(self, args, QueryItemType::QueryLimit); }
static PyObject* Offset(PyObject* self, PyObject* args) { return addValue(self, args, QueryItemType::QueryOffset); }
static PyObject* Debug(PyObject* self, PyObject* args) { return addValue(self, args, QueryItemType::QueryDebugLevel); }

static PyObject* Strict(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	unsigned mode = 0;
	if (!PyArg_ParseTuple(args, "kI", &queryWrapperAddr, &mode)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->Strict(StrictMode(mode));

	Py_RETURN_NONE;
}

namespace {
PyObject* modifier(PyObject* self, PyObject* args, QueryItemType type) {
	uintptr_t queryWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &queryWrapperAddr)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);
	query->Modifier(type);

	Py_RETURN_NONE;
}
} // namespace
static PyObject* Explain(PyObject* self, PyObject* args) { return modifier(self, args, QueryItemType::QueryExplain); }
static PyObject* WithRank(PyObject* self, PyObject* args) { return modifier(self, args, QueryItemType::QueryWithRank); }

static PyObject* DeleteQuery(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &queryWrapperAddr)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);
	size_t count = 0;
	auto err = query->DeleteQuery(count);

	return Py_BuildValue("isI", err.code(), err.what().c_str(), count);
}

namespace {
enum class ExecuteType { Select, Update };
static PyObject* executeQuery(PyObject* self, PyObject* args, ExecuteType type) {
	uintptr_t queryWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &queryWrapperAddr)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	auto qresWrapper = new QueryResultsWrapper(query->GetDB());
	Error err = errOK;
	switch (type) {
		case ExecuteType::Select:
			query->SelectQuery(*qresWrapper);
			break;
		case ExecuteType::Update:
			query->UpdateQuery(*qresWrapper);
			break;
		default:
			assert(false);
	}

	if (!err.ok()) {
		delete qresWrapper;

		return Py_BuildValue("iskI", err.code(), err.what().c_str(), 0, 0);
	}

	return Py_BuildValue("iskI", err.code(), err.what().c_str(), reinterpret_cast<uintptr_t>(qresWrapper), qresWrapper->Count());
}
} // namespace
static PyObject* SelectQuery(PyObject* self, PyObject* args) { return executeQuery(self, args, ExecuteType::Select); }
static PyObject* UpdateQuery(PyObject* self, PyObject* args) { return executeQuery(self, args, ExecuteType::Update); }

namespace {
static PyObject* setObject(PyObject* self, PyObject* args, QueryItemType type) {
	uintptr_t queryWrapperAddr = 0;
	char* field = nullptr;
	PyObject* valuesList = nullptr;  // borrowed ref after ParseTuple
	if (!PyArg_ParseTuple(args, "ksO!", &queryWrapperAddr, &field, &PyList_Type, &valuesList)) {
		return nullptr;
	}

	Py_INCREF(valuesList);

	std::vector<std::string> values;
	if (valuesList != nullptr) {
		try {
			values = PyObjectToJson(&valuesList);
		} catch (const Error& err) {
			Py_DECREF(valuesList);

			return pyErr(err);
		}
	}

	Py_DECREF(valuesList);

	if ((type == QueryItemType::QueryUpdateField) && (values.size() > 1)) {
		type = QueryItemType::QueryUpdateFieldV2;
	}
	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->SetObject(field, values, type);

	return pyErr(errOK);
}
} // namespace
static PyObject* SetObject(PyObject* self, PyObject* args) { return setObject(self, args, QueryItemType::QueryUpdateObject); }
static PyObject* Set(PyObject* self, PyObject* args) { return setObject(self, args, QueryItemType::QueryUpdateField); }

static PyObject* Drop(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* index = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &queryWrapperAddr, &index)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->Drop(index);

	Py_RETURN_NONE;
}

static PyObject* SetExpression(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* field = nullptr;
	char* value = nullptr;
	if (!PyArg_ParseTuple(args, "kss", &queryWrapperAddr, &field, &value)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->SetExpression(field, value);

	Py_RETURN_NONE;
}

static PyObject* Join(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	unsigned type = 0;
	unsigned index = 0;
	uintptr_t queryWrapperAddrJoin = 0;
	if (!PyArg_ParseTuple(args, "kIIk", &queryWrapperAddr, &type, &index, &queryWrapperAddrJoin)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);
	auto queryJoin = getWrapper<QueryWrapper>(queryWrapperAddrJoin);
	query->Join(JoinType(type), index, queryJoin);

	Py_RETURN_NONE;
}

static PyObject* Merge(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	uintptr_t queryWrapperAddrMerge = 0;
	if (!PyArg_ParseTuple(args, "kk", &queryWrapperAddr, &queryWrapperAddrMerge)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);
	auto queryMerge = getWrapper<QueryWrapper>(queryWrapperAddrMerge);
	query->Merge(queryMerge);

	Py_RETURN_NONE;
}

static PyObject* On(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* index = nullptr;
	unsigned condition = 0;
	char* joinIndex = nullptr;
	if (!PyArg_ParseTuple(args, "ksIs", &queryWrapperAddr, &index, &condition, &joinIndex)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	auto err = query->On(index, CondType(condition), joinIndex);
	return pyErr(err);
}

static PyObject* SelectFilter(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	PyObject* fieldsList = nullptr;  	// borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "kO!", &queryWrapperAddr, &PyList_Type, &fieldsList)) {
		return nullptr;
	}

	Py_XINCREF(fieldsList);

	std::vector<std::string> fields;
	if (fieldsList != nullptr) {
		try {
			fields = ParseStrListToStrVec(&fieldsList);
		} catch (const Error& err) {
			Py_DECREF(fieldsList);

			return pyErr(err);
		}
	}

	Py_XDECREF(fieldsList);

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->SelectFilter(fields);

	return pyErr(errOK);
}

static PyObject* AddFunctions(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	PyObject* functionsList = nullptr;  	// borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "kO!", &queryWrapperAddr, &PyList_Type, &functionsList)) {
		return nullptr;
	}

	Py_XINCREF(functionsList);

	std::vector<std::string> functions;
	if (functionsList != nullptr) {
		try {
			functions = ParseStrListToStrVec(&functionsList);
		} catch (const Error& err) {
			Py_DECREF(functionsList);

			return pyErr(err);
		}
	}

	Py_XDECREF(functionsList);

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->AddFunctions(functions);

	return pyErr(errOK);
}

static PyObject* AddEqualPosition(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	PyObject* equalPosesList = nullptr;  	// borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "kO!", &queryWrapperAddr, &PyList_Type, &equalPosesList)) {
		return nullptr;
	}

	Py_XINCREF(equalPosesList);

	std::vector<std::string> equalPoses;
	if (equalPosesList != nullptr) {
		try {
			equalPoses = ParseStrListToStrVec(&equalPosesList);
		} catch (const Error& err) {
			Py_DECREF(equalPosesList);

			return pyErr(err);
		}
	}

	Py_XDECREF(equalPosesList);

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);

	query->AddEqualPosition(equalPoses);

	return pyErr(errOK);
}

}  // namespace pyreindexer

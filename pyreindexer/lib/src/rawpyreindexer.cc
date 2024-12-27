#include "rawpyreindexer.h"

#include "tools/serializer.h"

#include "queryresults_wrapper.h"
#include "query_wrapper.h"
#include "pyobjtools.h"
#include "transaction_wrapper.h"

namespace pyreindexer {

using reindexer::Error;
using reindexer::IndexDef;
using reindexer::WrSerializer;

namespace {
uintptr_t initReindexer(const ReindexerConfig& cfg) {
	auto db = std::make_unique<DBInterface>(cfg);
	return reinterpret_cast<uintptr_t>(db.release());
}

template <typename T>
T* getWrapper(uintptr_t wrapperAddr) {
	return reinterpret_cast<T*>(wrapperAddr);
}

template <typename T>
void deleteWrapper(uintptr_t wrapperAddr) {
	T* queryWrapperPtr = getWrapper<T>(wrapperAddr);
	delete queryWrapperPtr;
}

PyObject* pyErr(const Error& err) { return Py_BuildValue("is", err.code(), err.what().c_str()); }

PyObject* queryResultsWrapperIterate(uintptr_t qresWrapperAddr) {
	QueryResultsWrapper* qresWrapper = getWrapper<QueryResultsWrapper>(qresWrapperAddr);

	WrSerializer wrSer;
	static const bool withHeaderLen = false;
	qresWrapper->GetItemJSON(wrSer, withHeaderLen);
	qresWrapper->Next();

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
	ReindexerConfig cfg;
	char* clientName = nullptr;
	int netTimeout = 0;
	unsigned enableCompression = 0;
	unsigned startSpecialThread = 0;
	unsigned syncRxCoroCount = 0;
	unsigned maxReplUpdatesSize = 0;
	if (!PyArg_ParseTuple(args, "iiiIIsIIif", &cfg.fetchAmount, &cfg.reconnectAttempts, &netTimeout,
						  &enableCompression, &startSpecialThread, &clientName, &syncRxCoroCount,
						  &maxReplUpdatesSize, &cfg.allocatorCacheLimit, &cfg.allocatorCachePart)) {
		return nullptr;
	}

	cfg.netTimeout = std::chrono::milliseconds(netTimeout);
	cfg.enableCompression = (enableCompression != 0);
	cfg.requestDedicatedThread = (startSpecialThread != 0);
	cfg.appName = clientName;
	cfg.syncRxCoroCount = syncRxCoroCount;
	cfg.maxReplUpdatesSize = maxReplUpdatesSize;

	uintptr_t rx = initReindexer(cfg);
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

	deleteWrapper<DBInterface>(rx);

	Py_RETURN_NONE;
}

static PyObject* Connect(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* dsn = nullptr;
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "ksI", &rx, &dsn, &timeout)) {
		return nullptr;
	}

	auto err = getWrapper<DBInterface>(rx)->Connect(dsn, std::chrono::milliseconds(timeout));
	return pyErr(err);
}

static PyObject* Select(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* query = nullptr;
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "ksI", &rx, &query, &timeout)) {
		return nullptr;
	}

	auto db = getWrapper<DBInterface>(rx);
	auto qresult = std::make_unique<QueryResultsWrapper>(db);
	auto err = qresult->Select(query, std::chrono::milliseconds(timeout));
	if (!err.ok()) {
		return Py_BuildValue("iskII", err.code(), err.what().c_str(), 0, 0);
	}

	const auto count = qresult->Count();
	const auto totalCount = qresult->TotalCount();
	return Py_BuildValue("iskII", err.code(), err.what().c_str(),
						 reinterpret_cast<uintptr_t>(qresult.release()), count, totalCount);
}

// namespace ----------------------------------------------------------------------------------------------------------

static PyObject* NamespaceOpen(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "ksI", &rx, &ns, &timeout)) {
		return nullptr;
	}

	auto err = getWrapper<DBInterface>(rx)->OpenNamespace(ns, std::chrono::milliseconds(timeout));
	return pyErr(err);
}

static PyObject* NamespaceClose(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "ksI", &rx, &ns, &timeout)) {
		return nullptr;
	}

	auto err = getWrapper<DBInterface>(rx)->CloseNamespace(ns, std::chrono::milliseconds(timeout));
	return pyErr(err);
}

static PyObject* NamespaceDrop(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "ksI", &rx, &ns, &timeout)) {
		return nullptr;
	}

	auto err = getWrapper<DBInterface>(rx)->DropNamespace(ns, std::chrono::milliseconds(timeout));
	return pyErr(err);
}

static PyObject* EnumNamespaces(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	unsigned enumAll = 0;
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "kII", &rx, &enumAll, &timeout)) {
		return nullptr;
	}

	std::vector<reindexer::NamespaceDef> nsDefs;
	auto err = getWrapper<DBInterface>(rx)->EnumNamespaces(nsDefs, reindexer::EnumNamespacesOpts().WithClosed(enumAll),
														   std::chrono::milliseconds(timeout));
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
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "ksO!I", &rx, &ns, &PyDict_Type, &indexDefDict, &timeout)) {
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
		err = getWrapper<DBInterface>(rx)->AddIndex(ns, indexDef, std::chrono::milliseconds(timeout));
	}
	return pyErr(err);
}

static PyObject* IndexUpdate(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	PyObject* indexDefDict = nullptr;  // borrowed ref after ParseTuple
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "ksO!I", &rx, &ns, &PyDict_Type, &indexDefDict, &timeout)) {
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
		err = getWrapper<DBInterface>(rx)->UpdateIndex(ns, indexDef, std::chrono::milliseconds(timeout));
	}
	return pyErr(err);
}

static PyObject* IndexDrop(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char *ns = nullptr, *indexName = nullptr;
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "kssI", &rx, &ns, &indexName, &timeout)) {
		return nullptr;
	}

	auto err = getWrapper<DBInterface>(rx)->DropIndex(ns, IndexDef(indexName), std::chrono::milliseconds(timeout));
	return pyErr(err);
}

// item ----------------------------------------------------------------------------------------------------------------

namespace {
PyObject* itemModify(PyObject* self, PyObject* args, ItemModifyMode mode) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	PyObject* itemDefDict = nullptr;   // borrowed ref after ParseTuple
	PyObject* preceptsList = nullptr;  // borrowed ref after ParseTuple if passed
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "ksO!|O!I", &rx, &ns, &PyDict_Type, &itemDefDict, &PyList_Type, &preceptsList,
						  &timeout)) {
		return nullptr;
	}

	Py_INCREF(itemDefDict);
	Py_XINCREF(preceptsList);

	auto item = getWrapper<DBInterface>(rx)->NewItem(ns, std::chrono::milliseconds(timeout));
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

	err = item.Unsafe().FromJSON(wrSer.Slice(), 0, mode == ModeDelete);
	if (!err.ok()) {
		Py_XDECREF(preceptsList);

		return pyErr(err);
	}

	if (preceptsList != nullptr && mode != ModeDelete) {
		std::vector<std::string> precepts;
		try {
			precepts = ParseStrListToStrVec<std::vector>(&preceptsList);
		} catch (const Error& err) {
			Py_DECREF(preceptsList);

			return pyErr(err);
		}

		item.SetPrecepts(precepts); // ToDo after migrate on v.4, do std::move
	}

	Py_XDECREF(preceptsList);

	switch (mode) {
		case ModeInsert:
			err = getWrapper<DBInterface>(rx)->Insert(ns, item, std::chrono::milliseconds(timeout));
			break;
		case ModeUpdate:
			err = getWrapper<DBInterface>(rx)->Update(ns, item, std::chrono::milliseconds(timeout));
			break;
		case ModeUpsert:
			err = getWrapper<DBInterface>(rx)->Upsert(ns, item, std::chrono::milliseconds(timeout));
			break;
		case ModeDelete:
			err = getWrapper<DBInterface>(rx)->Delete(ns, item, std::chrono::milliseconds(timeout));
			break;
		default:
			err = Error(ErrorCode::errLogic, "Unknown item modify mode");
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
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "ksssI", &rx, &ns, &key, &value, &timeout)) {
		return nullptr;
	}

	auto err = getWrapper<DBInterface>(rx)->PutMeta(ns, key, value, std::chrono::milliseconds(timeout));
	return pyErr(err);
}

static PyObject* GetMeta(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char *ns = nullptr, *key = nullptr;
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "kssI", &rx, &ns, &key, &timeout)) {
		return nullptr;
	}

	std::string value;
	auto err = getWrapper<DBInterface>(rx)->GetMeta(ns, key, value, std::chrono::milliseconds(timeout));
	return Py_BuildValue("iss", err.code(), err.what().c_str(), value.c_str());
}

static PyObject* DeleteMeta(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char *ns = nullptr, *key = nullptr;
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "kssI", &rx, &ns, &key, &timeout)) {
		return nullptr;
	}

	auto err = getWrapper<DBInterface>(rx)->DeleteMeta(ns, key, std::chrono::milliseconds(timeout));
	return pyErr(err);
}

static PyObject* EnumMeta(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "ksI", &rx, &ns, &timeout)) {
		return nullptr;
	}

	std::vector<std::string> keys;
	auto err = getWrapper<DBInterface>(rx)->EnumMeta(ns, keys, std::chrono::milliseconds(timeout));
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

	auto err = getWrapper<QueryResultsWrapper>(qresWrapperAddr)->Status();
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

	deleteWrapper<QueryResultsWrapper>(qresWrapperAddr);

	Py_RETURN_NONE;
}

static PyObject* GetAggregationResults(PyObject* self, PyObject* args) {
	uintptr_t qresWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &qresWrapperAddr)) {
		return nullptr;
	}

	const auto& aggResults = getWrapper<QueryResultsWrapper>(qresWrapperAddr)->GetAggregationResults();
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

	const auto& explainResults = getWrapper<QueryResultsWrapper>(qresWrapperAddr)->GetExplainResults();

	return Py_BuildValue("iss", errOK, "", explainResults.c_str());
}

// transaction ---------------------------------------------------------------------------------------------------------

static PyObject* NewTransaction(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "ksI", &rx, &ns, &timeout)) {
		return nullptr;
	}

	auto db = getWrapper<DBInterface>(rx);
	auto transaction = std::make_unique<TransactionWrapper>(db);
	auto err = transaction->Start(ns, std::chrono::milliseconds(timeout));
	if (!err.ok()) {
		return Py_BuildValue("isk", err.code(), err.what().c_str(), 0);
	}

	return Py_BuildValue("isk", err.code(), err.what().c_str(), reinterpret_cast<uintptr_t>(transaction.release()));
}

namespace {
PyObject* modifyTransaction(PyObject* self, PyObject* args, ItemModifyMode mode) {
	uintptr_t transactionWrapperAddr = 0;
	PyObject* defDict = nullptr;   // borrowed ref after ParseTuple
	PyObject* preceptsList = nullptr;  // borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "kO!|O!", &transactionWrapperAddr, &PyDict_Type, &defDict, &PyList_Type, &preceptsList)) {
		return nullptr;
	}

	Py_INCREF(defDict);
	Py_XINCREF(preceptsList);

	auto transaction = getWrapper<TransactionWrapper>(transactionWrapperAddr);

	auto item = transaction->NewItem();
	auto err = item.Status();
	if (!err.ok()) {
		Py_DECREF(defDict);
		Py_XDECREF(preceptsList);

		return pyErr(err);
	}

	WrSerializer wrSer;

	try {
		PyObjectToJson(&defDict, wrSer);
	} catch (const Error& err) {
		Py_DECREF(defDict);
		Py_XDECREF(preceptsList);

		return pyErr(err);
	}

	Py_DECREF(defDict);

	err = item.FromJSON(wrSer.Slice(), 0, mode == ModeDelete);
	if (!err.ok()) {
		Py_XDECREF(preceptsList);

		return pyErr(err);
	}

	if (preceptsList != nullptr && mode != ModeDelete) {
		std::vector<std::string> precepts;

		try {
			precepts = ParseStrListToStrVec<std::vector>(&preceptsList);
		} catch (const Error& err) {
			Py_DECREF(preceptsList);

			return pyErr(err);
		}

		item.SetPrecepts(precepts); // ToDo after migrate on v.4, do std::move
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
			return pyErr(Error(ErrorCode::errLogic, "Unknown item modify transaction mode"));
	}

	return nullptr;
}
} // namespace
static PyObject* InsertTransaction(PyObject* self, PyObject* args) { return modifyTransaction(self, args, ModeInsert); }
static PyObject* UpdateTransaction(PyObject* self, PyObject* args) { return modifyTransaction(self, args, ModeUpdate); }
static PyObject* UpsertTransaction(PyObject* self, PyObject* args) { return modifyTransaction(self, args, ModeUpsert); }
static PyObject* DeleteTransaction(PyObject* self, PyObject* args) { return modifyTransaction(self, args, ModeDelete); }

static PyObject* CommitTransaction(PyObject* self, PyObject* args) {
	uintptr_t transactionWrapperAddr = 0;
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "kI", &transactionWrapperAddr, &timeout)) {
		return nullptr;
	}

	size_t count = 0;
	auto err = getWrapper<TransactionWrapper>(transactionWrapperAddr)->Commit(count, std::chrono::milliseconds(timeout));

	deleteWrapper<TransactionWrapper>(transactionWrapperAddr); // free memory

	return Py_BuildValue("isI", err.code(), err.what().c_str(), count);
}

static PyObject* RollbackTransaction(PyObject* self, PyObject* args) {
	uintptr_t transactionWrapperAddr = 0;
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "kI", &transactionWrapperAddr, &timeout)) {
		return nullptr;
	}

	auto err = getWrapper<TransactionWrapper>(transactionWrapperAddr)->Rollback(std::chrono::milliseconds(timeout));

	deleteWrapper<TransactionWrapper>(transactionWrapperAddr); // free memory

	return pyErr(err);
}

// query ---------------------------------------------------------------------------------------------------------------

static PyObject* CreateQuery(PyObject* self, PyObject* args) {
	uintptr_t rx = 0;
	char* ns = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &rx, &ns)) {
		return nullptr;
	}

	auto db = getWrapper<DBInterface>(rx);
	auto query = std::make_unique<QueryWrapper>(db, ns);
	return Py_BuildValue("isK", errOK, "", reinterpret_cast<uintptr_t>(query.release()));
}

static PyObject* DestroyQuery(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &queryWrapperAddr)) {
		return nullptr;
	}

	deleteWrapper<QueryWrapper>(queryWrapperAddr);

	Py_RETURN_NONE;
}

static PyObject* Where(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* index = nullptr;
	unsigned condition = 0;
	PyObject* keysList = nullptr;  // borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "ksIO!", &queryWrapperAddr, &index, &condition, &PyList_Type, &keysList)) {
		return nullptr;
	}

	Py_XINCREF(keysList);

	reindexer::VariantArray keys;
	if (keysList != nullptr) {
		try {
			keys = ParseListToVec(&keysList);
		} catch (const Error& err) {
			Py_DECREF(keysList);

			return pyErr(err);
		}
	}

	Py_XDECREF(keysList);

	getWrapper<QueryWrapper>(queryWrapperAddr)->Where(index, CondType(condition), keys);

	return pyErr({});
}

static PyObject* WhereSubQuery(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	uintptr_t subQueryWrapperAddr = 0;
	unsigned cond = 0;
	PyObject* keysList = nullptr;  // borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "kkIO!", &queryWrapperAddr, &subQueryWrapperAddr, &cond, &PyList_Type, &keysList)) {
		return nullptr;
	}

	Py_XINCREF(keysList);

	reindexer::VariantArray keys;
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
	query->WhereSubQuery(*subQuery, CondType(cond), keys);

	return pyErr({});
}

static PyObject* WhereFieldSubQuery(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* index = nullptr;
	unsigned condition = 0;
	uintptr_t subQueryWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "ksIk", &queryWrapperAddr, &index, &condition, &subQueryWrapperAddr)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);
	auto subQuery = getWrapper<QueryWrapper>(subQueryWrapperAddr);

	query->WhereFieldSubQuery(index, CondType(condition), *subQuery);

	Py_RETURN_NONE;
}

static PyObject* WhereUUID(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* index = nullptr;
	unsigned condition = 0;
	PyObject* keysList = nullptr;  // borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "ksIO!", &queryWrapperAddr, &index, &condition, &PyList_Type, &keysList)) {
		return nullptr;
	}

	Py_XINCREF(keysList);

	reindexer::h_vector<std::string, 2> keys;
	if (keysList != nullptr) {
		try {
			keys = ParseStrListToStrVec(&keysList);
		} catch (const Error& err) {
			Py_DECREF(keysList);

			return pyErr(err);
		}
	}

	Py_XDECREF(keysList);

	getWrapper<QueryWrapper>(queryWrapperAddr)->WhereUUID(index, CondType(condition), keys);

	return pyErr({});
}

static PyObject* WhereBetweenFields(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* first_field = nullptr;
	unsigned condition = 0;
	char* second_field = nullptr;
	if (!PyArg_ParseTuple(args, "ksIs", &queryWrapperAddr, &first_field, &condition, &second_field)) {
		return nullptr;
	}

	getWrapper<QueryWrapper>(queryWrapperAddr)->WhereBetweenFields(first_field, CondType(condition), second_field);

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

	getWrapper<QueryWrapper>(queryWrapperAddr)->DWithin(index, x, y, distance);

	Py_RETURN_NONE;
}

namespace {
PyObject* aggregate(PyObject* self, PyObject* args, AggType type) {
	uintptr_t queryWrapperAddr = 0;
	char* field = nullptr;
	if (!PyArg_ParseTuple(args, "ks", &queryWrapperAddr, &field)) {
		return nullptr;
	}

	getWrapper<QueryWrapper>(queryWrapperAddr)->Aggregate(field, type);

	Py_RETURN_NONE;
}
} // namespace
static PyObject* AggregateDistinct(PyObject* self, PyObject* args) {
	return aggregate(self, args, AggType::AggDistinct);
}
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

	getWrapper<QueryWrapper>(queryWrapperAddr)->AddValue(type, value);

	Py_RETURN_NONE;
}
} // namespace
static PyObject* AggregationLimit(PyObject* self, PyObject* args) {
	return addValue(self, args, QueryItemType::QueryAggregationLimit);
}
static PyObject* AggregationOffset(PyObject* self, PyObject* args) {
	return addValue(self, args, QueryItemType::QueryAggregationOffset);
}

static PyObject* AggregationSort(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* field = nullptr;
	unsigned desc = 0;
	if (!PyArg_ParseTuple(args, "ksI", &queryWrapperAddr, &field, &desc)) {
		return nullptr;
	}

	getWrapper<QueryWrapper>(queryWrapperAddr)->AggregationSort(field, (desc != 0));

	return pyErr({});
}

static PyObject* Aggregation(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	PyObject* fieldsList = nullptr;  // borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "kO!", &queryWrapperAddr, &PyList_Type, &fieldsList)) {
		return nullptr;
	}

	Py_XINCREF(fieldsList);

	reindexer::h_vector<std::string, 2> fields;
	if (fieldsList != nullptr) {
		try {
			fields = ParseStrListToStrVec(&fieldsList);
		} catch (const Error& err) {
			Py_DECREF(fieldsList);

			return pyErr(err);
		}
	}

	Py_XDECREF(fieldsList);

	getWrapper<QueryWrapper>(queryWrapperAddr)->Aggregation(fields);

	return pyErr({});
}

static PyObject* Sort(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* index = nullptr;
	unsigned desc = 0;
	PyObject* sortValuesList = nullptr;  // borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "ksIO!", &queryWrapperAddr, &index, &desc, &PyList_Type, &sortValuesList)) {
		return nullptr;
	}

	Py_XINCREF(sortValuesList);

	reindexer::VariantArray sortValues;
	if (sortValuesList != nullptr) {
		try {
			sortValues = ParseListToVec(&sortValuesList);
		} catch (const Error& err) {
			Py_DECREF(sortValuesList);

			return pyErr(err);
		}
	}

	Py_XDECREF(sortValuesList);

	getWrapper<QueryWrapper>(queryWrapperAddr)->Sort(index, (desc != 0), sortValues);

	return pyErr({});
}

namespace {
PyObject* logOp(PyObject* self, PyObject* args, OpType opID) {
	uintptr_t queryWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &queryWrapperAddr)) {
		return nullptr;
	}

	getWrapper<QueryWrapper>(queryWrapperAddr)->LogOp(opID);

	Py_RETURN_NONE;
}
} // namespace
static PyObject* And(PyObject* self, PyObject* args) { return logOp(self, args, OpType::OpAnd); }
static PyObject* Or(PyObject* self, PyObject* args) { return logOp(self, args, OpType::OpOr); }
static PyObject* Not(PyObject* self, PyObject* args) { return logOp(self, args, OpType::OpNot); }

namespace {
static PyObject* total(PyObject* self, PyObject* args, CalcTotalMode mode) {
	uintptr_t queryWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &queryWrapperAddr)) {
		return nullptr;
	}

	getWrapper<QueryWrapper>(queryWrapperAddr)->Total(mode);

	Py_RETURN_NONE;
}
} // namespace
static PyObject* ReqTotal(PyObject* self, PyObject* args) {
	return total(self, args, CalcTotalMode::ModeAccurateTotal);
}
static PyObject* CachedTotal(PyObject* self, PyObject* args) {
	return total(self, args, CalcTotalMode::ModeCachedTotal);
}

static PyObject* Limit(PyObject* self, PyObject* args) { return addValue(self, args, QueryItemType::QueryLimit); }
static PyObject* Offset(PyObject* self, PyObject* args) { return addValue(self, args, QueryItemType::QueryOffset); }
static PyObject* Debug(PyObject* self, PyObject* args) { return addValue(self, args, QueryItemType::QueryDebugLevel); }

static PyObject* Strict(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	unsigned mode = 0;
	if (!PyArg_ParseTuple(args, "kI", &queryWrapperAddr, &mode)) {
		return nullptr;
	}

	getWrapper<QueryWrapper>(queryWrapperAddr)->AddValue(QueryItemType::QueryStrictMode, mode);

	Py_RETURN_NONE;
}

namespace {
PyObject* modifier(PyObject* self, PyObject* args, QueryItemType type) {
	uintptr_t queryWrapperAddr = 0;
	if (!PyArg_ParseTuple(args, "k", &queryWrapperAddr)) {
		return nullptr;
	}

	getWrapper<QueryWrapper>(queryWrapperAddr)->Modifier(type);

	Py_RETURN_NONE;
}
} // namespace
static PyObject* Explain(PyObject* self, PyObject* args) { return modifier(self, args, QueryItemType::QueryExplain); }
static PyObject* WithRank(PyObject* self, PyObject* args) { return modifier(self, args, QueryItemType::QueryWithRank); }

static PyObject* DeleteQuery(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "kI", &queryWrapperAddr, &timeout)) {
		return nullptr;
	}

	size_t count = 0;
	auto err = getWrapper<QueryWrapper>(queryWrapperAddr)->DeleteQuery(count, std::chrono::milliseconds(timeout));

	return Py_BuildValue("isI", err.code(), err.what().c_str(), count);
}

namespace {
enum class ExecuteType { Select, Update };
static PyObject* executeQuery(PyObject* self, PyObject* args, ExecuteType type) {
	uintptr_t queryWrapperAddr = 0;
	unsigned timeout = 0;
	if (!PyArg_ParseTuple(args, "kI", &queryWrapperAddr, &timeout)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);
	std::unique_ptr<QueryResultsWrapper> qresult;
	Error err;
	switch (type) {
		case ExecuteType::Select:
			err = query->SelectQuery(qresult, std::chrono::milliseconds(timeout));
			break;
		case ExecuteType::Update:
			err = query->UpdateQuery(qresult, std::chrono::milliseconds(timeout));
			break;
		default:
			return pyErr(Error(ErrorCode::errLogic, "Unknown query execute mode"));
	}

	if (!err.ok()) {
		return Py_BuildValue("iskII", err.code(), err.what().c_str(), 0, 0, 0);
	}

	const auto count = qresult->Count();
	const auto totalCount = qresult->TotalCount();
	return Py_BuildValue("iskII", err.code(), err.what().c_str(),
						 reinterpret_cast<uintptr_t>(qresult.release()), count, totalCount);
}
} // namespace
static PyObject* SelectQuery(PyObject* self, PyObject* args) { return executeQuery(self, args, ExecuteType::Select); }
static PyObject* UpdateQuery(PyObject* self, PyObject* args) { return executeQuery(self, args, ExecuteType::Update); }

static PyObject* SetObject(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* field = nullptr;
	PyObject* valuesList = nullptr;  // borrowed ref after ParseTuple
	if (!PyArg_ParseTuple(args, "ksO!", &queryWrapperAddr, &field, &PyList_Type, &valuesList)) {
		return nullptr;
	}

	Py_INCREF(valuesList);

	reindexer::h_vector<std::string, 2> values;
	if (valuesList != nullptr) {
		try {
			values = PyObjectToJson(&valuesList);
		} catch (const Error& err) {
			Py_DECREF(valuesList);

			return pyErr(err);
		}
	}

	Py_DECREF(valuesList);

	getWrapper<QueryWrapper>(queryWrapperAddr)->SetObject(field, values);

	return pyErr({});
}

static PyObject* Set(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	char* field = nullptr;
	PyObject* valuesList = nullptr;  // borrowed ref after ParseTuple
	if (!PyArg_ParseTuple(args, "ksO!", &queryWrapperAddr, &field, &PyList_Type, &valuesList)) {
		return nullptr;
	}

	Py_INCREF(valuesList);

	reindexer::VariantArray values;
	if (valuesList != nullptr) {
		try {
			values = ParseListToVec(&valuesList);
		} catch (const Error& err) {
			Py_DECREF(valuesList);

			return pyErr(err);
		}
	}

	Py_DECREF(valuesList);

	getWrapper<QueryWrapper>(queryWrapperAddr)->Set(field, values, QueryWrapper::IsExpression::No);

	return pyErr({});
}

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

	query->Set(field, {reindexer::Variant{value}}, QueryWrapper::IsExpression::Yes);

	Py_RETURN_NONE;
}

static PyObject* Join(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	unsigned type = 0;
	uintptr_t queryWrapperAddrJoin = 0;
	if (!PyArg_ParseTuple(args, "kIk", &queryWrapperAddr, &type, &queryWrapperAddrJoin)) {
		return nullptr;
	}

	auto query = getWrapper<QueryWrapper>(queryWrapperAddr);
	auto queryJoin = getWrapper<QueryWrapper>(queryWrapperAddrJoin);
	query->Join(JoinType(type), queryJoin);

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

	auto err = getWrapper<QueryWrapper>(queryWrapperAddr)->On(index, CondType(condition), joinIndex);
	return pyErr(err);
}

static PyObject* SelectFilter(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	PyObject* fieldsList = nullptr;  // borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "kO!", &queryWrapperAddr, &PyList_Type, &fieldsList)) {
		return nullptr;
	}

	Py_XINCREF(fieldsList);

	reindexer::h_vector<std::string, 2> fields;
	if (fieldsList != nullptr) {
		try {
			fields = ParseStrListToStrVec(&fieldsList);
		} catch (const Error& err) {
			Py_DECREF(fieldsList);

			return pyErr(err);
		}
	}

	Py_XDECREF(fieldsList);

	getWrapper<QueryWrapper>(queryWrapperAddr)->SelectFilter(fields);

	return pyErr({});
}

static PyObject* AddFunctions(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	PyObject* functionsList = nullptr;  // borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "kO!", &queryWrapperAddr, &PyList_Type, &functionsList)) {
		return nullptr;
	}

	Py_XINCREF(functionsList);

	reindexer::h_vector<std::string, 2> functions;
	if (functionsList != nullptr) {
		try {
			functions = ParseStrListToStrVec(&functionsList);
		} catch (const Error& err) {
			Py_DECREF(functionsList);

			return pyErr(err);
		}
	}

	Py_XDECREF(functionsList);

	getWrapper<QueryWrapper>(queryWrapperAddr)->AddFunctions(functions);

	return pyErr({});
}

static PyObject* AddEqualPosition(PyObject* self, PyObject* args) {
	uintptr_t queryWrapperAddr = 0;
	PyObject* equalPosesList = nullptr;  // borrowed ref after ParseTuple if passed
	if (!PyArg_ParseTuple(args, "kO!", &queryWrapperAddr, &PyList_Type, &equalPosesList)) {
		return nullptr;
	}

	Py_XINCREF(equalPosesList);

	reindexer::h_vector<std::string, 2> equalPoses;
	if (equalPosesList != nullptr) {
		try {
			equalPoses = ParseStrListToStrVec(&equalPosesList);
		} catch (const Error& err) {
			Py_DECREF(equalPosesList);

			return pyErr(err);
		}
	}

	Py_XDECREF(equalPosesList);

	getWrapper<QueryWrapper>(queryWrapperAddr)->AddEqualPosition(equalPoses);

	return pyErr({});
}

}  // namespace pyreindexer

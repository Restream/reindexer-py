#include "reindexerinterface.h"
#include "client/reindexer.h"
#include "core/reindexer.h"
#include "core/type_consts.h"
#include "queryresults_wrapper.h"
#include "transaction_wrapper.h"

namespace pyreindexer {
namespace {
	const int QRESULTS_FLAGS = kResultsJson | kResultsWithJoined;
}

namespace {
reindexer::client::ReindexerConfig makeClientConfig(const ReindexerConfig& cfg) {
	reindexer::client::ReindexerConfig config;
	config.FetchAmount = cfg.fetchAmount;
	config.ReconnectAttempts = cfg.reconnectAttempts;
	config.NetTimeout = cfg.netTimeout;
	config.EnableCompression = cfg.enableCompression;
	config.RequestDedicatedThread = cfg.requestDedicatedThread;
	config.AppName = cfg.appName;
	config.SyncRxCoroCount = cfg.syncRxCoroCount;
	//config.ReplToken = cfg.replToken; // NOTE: now not used
	return config;
}
} // namespace

template <>
ReindexerInterface<reindexer::Reindexer>::ReindexerInterface(const ReindexerConfig& cfg)
	: db_(reindexer::ReindexerConfig().WithUpdatesSize(cfg.maxReplUpdatesSize)
									  .WithAllocatorCacheLimits(cfg.allocatorCacheLimit, cfg.allocatorCachePart))
{ }

template <>
ReindexerInterface<reindexer::client::Reindexer>::ReindexerInterface(const ReindexerConfig& cfg)
	: db_(makeClientConfig(cfg))
{ }

template <>
ReindexerInterface<reindexer::Reindexer>::~ReindexerInterface() {
}

template <>
ReindexerInterface<reindexer::client::Reindexer>::~ReindexerInterface() {
	db_.Stop();
}

template <>
Error ReindexerInterface<reindexer::Reindexer>::Connect(const std::string& dsn, std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).Connect(dsn);
}

template <>
Error ReindexerInterface<reindexer::client::Reindexer>::Connect(
		const std::string& dsn, std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).Connect(dsn, reindexer::client::ConnectOpts().CreateDBIfMissing());
}

template <typename DBT>
Error ReindexerInterface<DBT>::OpenNamespace(std::string_view ns, std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).OpenNamespace(ns);
}

template <typename DBT>
Error ReindexerInterface<DBT>::CloseNamespace(std::string_view ns, std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).CloseNamespace(ns);
}

template <typename DBT>
Error ReindexerInterface<DBT>::DropNamespace(std::string_view ns, std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).DropNamespace(ns);
}

template <typename DBT>
Error ReindexerInterface<DBT>::AddIndex(std::string_view ns, const IndexDef& idx, std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).AddIndex(ns, idx);
}

template <typename DBT>
Error ReindexerInterface<DBT>::UpdateIndex(std::string_view ns, const IndexDef& idx,
										   std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).UpdateIndex(ns, idx);
}

template <typename DBT>
Error ReindexerInterface<DBT>::DropIndex(std::string_view ns, const IndexDef& idx, std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).DropIndex(ns, idx);
}

template <typename DBT>
Error ReindexerInterface<DBT>::NewItem(std::string_view ns, typename DBT::ItemT& item,
									   std::chrono::milliseconds timeout) {
	item = db_.WithTimeout(timeout).NewItem(ns);
	return item.Status();
}

template <typename DBT>
Error ReindexerInterface<DBT>::Insert(std::string_view ns, typename DBT::ItemT& item,
									  std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).Insert(ns, item);
}

template <typename DBT>
Error ReindexerInterface<DBT>::Upsert(std::string_view ns, typename DBT::ItemT& item,
									  std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).Upsert(ns, item);
}

template <typename DBT>
Error ReindexerInterface<DBT>::Update(std::string_view ns, typename DBT::ItemT& item,
									  std::chrono::milliseconds timeout)
 {
	return db_.WithTimeout(timeout).Update(ns, item);
}

template <typename DBT>
Error ReindexerInterface<DBT>::Delete(std::string_view ns, typename DBT::ItemT& item,
									  std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).Delete(ns, item);
}

template <typename DBT>
Error ReindexerInterface<DBT>::PutMeta(std::string_view ns, const std::string& key, std::string_view data,
									   std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).PutMeta(ns, key, data);
}

template <typename DBT>
Error ReindexerInterface<DBT>::GetMeta(std::string_view ns, const std::string& key, std::string& data,
									   std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).GetMeta(ns, key, data);
}

template <typename DBT>
Error ReindexerInterface<DBT>::DeleteMeta(std::string_view ns, const std::string& key,
										  std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).DeleteMeta(ns, key);
}

template <typename DBT>
Error ReindexerInterface<DBT>::EnumMeta(std::string_view ns, std::vector<std::string>& keys,
										std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).EnumMeta(ns, keys);
}

template <typename DBT>
Error ReindexerInterface<DBT>::ExecSQL(std::string_view query, QueryResultsWrapper& result,
									   std::chrono::milliseconds timeout) {
	typename DBT::QueryResultsT qres(QRESULTS_FLAGS);
	auto err = db_.WithTimeout(timeout).ExecSQL(query, qres);
	result.Wrap(std::move(qres));
	return err;
}

template <typename DBT>
Error ReindexerInterface<DBT>::EnumNamespaces(std::vector<NamespaceDef>& defs, EnumNamespacesOpts opts,
											  std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).EnumNamespaces(defs, opts);
}

template <typename DBT>
Error ReindexerInterface<DBT>::FetchResults(QueryResultsWrapper& result) {
	result.FetchResults();
	return {};
}

template <typename DBT>
Error ReindexerInterface<DBT>::StartTransaction(std::string_view ns, TransactionWrapper& transactionWrapper,
												std::chrono::milliseconds timeout) {
	auto transaction = db_.WithTimeout(timeout).NewTransaction(ns);
	auto err = transaction.Status();
	transactionWrapper.Wrap(std::move(transaction));
	return err;
}

template <typename DBT>
Error ReindexerInterface<DBT>::NewItem(typename DBT::TransactionT& transaction, typename DBT::ItemT& item) {
	item = transaction.NewItem();
	return item.Status();
}

template <typename DBT>
Error ReindexerInterface<DBT>::Modify(typename DBT::TransactionT& transaction, typename DBT::ItemT&& item,
									  ItemModifyMode mode) {
	return transaction.Modify(std::move(item), mode);
}

template <typename DBT>
Error ReindexerInterface<DBT>::Modify(typename DBT::TransactionT& transaction, reindexer::Query&& query) {
	return transaction.Modify(std::move(query));
}

template <typename DBT>
Error ReindexerInterface<DBT>::CommitTransaction(typename DBT::TransactionT& transaction, size_t& count,
												 std::chrono::milliseconds timeout) {
	typename DBT::QueryResultsT qres(QRESULTS_FLAGS);
	auto err = db_.WithTimeout(timeout).CommitTransaction(transaction, qres);
	count = qres.Count();
	return err;
}

template <typename DBT>
Error ReindexerInterface<DBT>::RollbackTransaction(typename DBT::TransactionT& transaction,
												   std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).RollBackTransaction(transaction);
}

template <typename DBT>
Error ReindexerInterface<DBT>::SelectQuery(const Query& query, QueryResultsWrapper& result,
										   std::chrono::milliseconds timeout) {
	typename DBT::QueryResultsT qres(QRESULTS_FLAGS);
	auto err = db_.WithTimeout(timeout).Select(query, qres);
	result.Wrap(std::move(qres));
	return err;
}

template <typename DBT>
Error ReindexerInterface<DBT>::DeleteQuery(const Query& query, size_t& count, std::chrono::milliseconds timeout) {
	typename DBT::QueryResultsT qres;
	auto err = db_.WithTimeout(timeout).Delete(query, qres);
	count = qres.Count();
	return err;
}

template <typename DBT>
Error ReindexerInterface<DBT>::UpdateQuery(const Query& query, QueryResultsWrapper& result,
										   std::chrono::milliseconds timeout) {
	typename DBT::QueryResultsT qres(QRESULTS_FLAGS);
	auto err = db_.WithTimeout(timeout).Update(query, qres);
	result.Wrap(std::move(qres));
	return err;
}

#ifdef PYREINDEXER_CPROTO
template class ReindexerInterface<reindexer::client::Reindexer>;
#else
template class ReindexerInterface<reindexer::Reindexer>;
#endif

}  // namespace pyreindexer

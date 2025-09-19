#pragma once

#include <chrono>
#include "core/query/query.h"
#include "core/indexdef.h"
#include "core/namespacedef.h"
#include "tools/errors.h"

namespace pyreindexer {

using reindexer::Error;
using reindexer::Query;
using reindexer::IndexDef;
using reindexer::NamespaceDef;
using reindexer::EnumNamespacesOpts;

class QueryResultsWrapper;
class TransactionWrapper;
class ICommand;

struct ReindexerConfig {
	int fetchAmount{1000};
	int reconnectAttempts{0};
	std::chrono::milliseconds netTimeout{0};
	bool enableCompression{false};
	bool requestDedicatedThread{false};
	std::string appName;
	unsigned int syncRxCoroCount{10};

	size_t maxReplUpdatesSize{1024 * 1024 * 1024};
	int64_t allocatorCacheLimit{-1};
	float allocatorCachePart{-1.0};
};

template <typename DBT>
class ReindexerInterface {
public:
	ReindexerInterface(const ReindexerConfig& cfg);
	~ReindexerInterface();

	Error Connect(const std::string& dsn, std::chrono::milliseconds timeout);

	Error OpenNamespace(std::string_view ns, std::chrono::milliseconds timeout);
	Error CloseNamespace(std::string_view ns, std::chrono::milliseconds timeout);
	Error DropNamespace(std::string_view ns, std::chrono::milliseconds timeout);

	Error AddIndex(std::string_view ns, const IndexDef& idx, std::chrono::milliseconds timeout);
	Error UpdateIndex(std::string_view ns, const IndexDef& idx, std::chrono::milliseconds timeout);
	Error DropIndex(std::string_view ns, const IndexDef& idx, std::chrono::milliseconds timeout);

	Error NewItem(std::string_view ns, typename DBT::ItemT& item, std::chrono::milliseconds timeout);
	Error Insert(std::string_view ns, typename DBT::ItemT& item, std::chrono::milliseconds timeout);
	Error Upsert(std::string_view ns, typename DBT::ItemT& item, std::chrono::milliseconds timeout);
	Error Update(std::string_view ns, typename DBT::ItemT& item, std::chrono::milliseconds timeout);
	Error Delete(std::string_view ns, typename DBT::ItemT& item, std::chrono::milliseconds timeout);

	Error PutMeta(std::string_view ns, const std::string& key, std::string_view data,
				  std::chrono::milliseconds timeout);
	Error GetMeta(std::string_view ns, const std::string& key, std::string& data, std::chrono::milliseconds timeout);
	Error DeleteMeta(std::string_view ns, const std::string& key, std::chrono::milliseconds timeout);
	Error EnumMeta(std::string_view ns, std::vector<std::string>& keys, std::chrono::milliseconds timeout);

	Error ExecSQL(std::string_view query, QueryResultsWrapper& result, std::chrono::milliseconds timeout);
	Error EnumNamespaces(std::vector<NamespaceDef>& defs, EnumNamespacesOpts opts, std::chrono::milliseconds timeout);
	Error FetchResults(QueryResultsWrapper& result);

	Error StartTransaction(std::string_view ns, TransactionWrapper& transactionWrapper,
						   std::chrono::milliseconds timeout);
	Error NewItem(typename DBT::TransactionT& transaction, typename DBT::ItemT& item);
	Error Modify(typename DBT::TransactionT& transaction, typename DBT::ItemT&& item, ItemModifyMode mode);
	Error Modify(typename DBT::TransactionT& transaction, Query&& query);
	Error CommitTransaction(typename DBT::TransactionT& transaction, size_t& count, std::chrono::milliseconds timeout);
	Error RollbackTransaction(typename DBT::TransactionT& transaction, std::chrono::milliseconds timeout);

	Error SelectQuery(const Query& query, QueryResultsWrapper& result, std::chrono::milliseconds timeout);
	Error DeleteQuery(const Query& query, size_t& count, std::chrono::milliseconds timeout);
	Error UpdateQuery(const Query& query, QueryResultsWrapper& result, std::chrono::milliseconds timeout);

private:
	DBT db_;
	std::chrono::milliseconds timeout_{0};
};

}  // namespace pyreindexer

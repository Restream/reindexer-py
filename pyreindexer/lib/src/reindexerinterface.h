#pragma once

#include <chrono>
#include <condition_variable>
#include <thread>
#include "core/query/query.h"
#include "core/indexdef.h"
#include "core/namespacedef.h"
#include "coroutine/channel.h"
#include "net/ev/ev.h"
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

	Error Connect(const std::string& dsn, std::chrono::milliseconds timeout) {
		return execute([this, &dsn, timeout] { return connect(dsn, timeout); });
	}
	Error OpenNamespace(std::string_view ns, std::chrono::milliseconds timeout) {
		return execute([this, ns, timeout] { return openNamespace(ns, timeout); });
	}
	Error CloseNamespace(std::string_view ns, std::chrono::milliseconds timeout) {
		return execute([this, ns, timeout] { return closeNamespace(ns, timeout); });
	}
	Error DropNamespace(std::string_view ns, std::chrono::milliseconds timeout) {
		return execute([this, ns, timeout] { return dropNamespace(ns, timeout); });
	}
	Error AddIndex(std::string_view ns, const IndexDef& idx, std::chrono::milliseconds timeout) {
		return execute([this, ns, &idx, timeout] { return addIndex(ns, idx, timeout); });
	}
	Error UpdateIndex(std::string_view ns, const IndexDef& idx, std::chrono::milliseconds timeout) {
		return execute([this, ns, &idx, timeout] { return updateIndex(ns, idx, timeout); });
	}
	Error DropIndex(std::string_view ns, const IndexDef& idx, std::chrono::milliseconds timeout) {
		return execute([this, ns, &idx, timeout] { return dropIndex(ns, idx, timeout); });
	}
	typename DBT::ItemT NewItem(std::string_view ns, std::chrono::milliseconds timeout) {
		typename DBT::ItemT item;
		execute([this, ns, &item, timeout] {
			item = newItem(ns, timeout);
			return item.Status();
		});
		return item;
	}
	Error Insert(std::string_view ns, typename DBT::ItemT& item, std::chrono::milliseconds timeout) {
		return execute([this, ns, &item, timeout] { return insert(ns, item, timeout); });
	}
	Error Upsert(std::string_view ns, typename DBT::ItemT& item, std::chrono::milliseconds timeout) {
		return execute([this, ns, &item, timeout] { return upsert(ns, item, timeout); });
	}
	Error Update(std::string_view ns, typename DBT::ItemT& item, std::chrono::milliseconds timeout) {
		return execute([this, ns, &item, timeout] { return update(ns, item, timeout); });
	}
	Error Delete(std::string_view ns, typename DBT::ItemT& item, std::chrono::milliseconds timeout) {
		return execute([this, ns, &item, timeout] { return deleteItem(ns, item, timeout); });
	}
	Error PutMeta(std::string_view ns, const std::string& key, std::string_view data,
				  std::chrono::milliseconds timeout) {
		return execute([this, ns, &key, data, timeout] { return putMeta(ns, key, data, timeout); });
	}
	Error GetMeta(std::string_view ns, const std::string& key, std::string& data, std::chrono::milliseconds timeout) {
		return execute([this, ns, &key, &data, timeout] { return getMeta(ns, key, data, timeout); });
	}
	Error DeleteMeta(std::string_view ns, const std::string& key, std::chrono::milliseconds timeout) {
		return execute([this, ns, &key, timeout] { return deleteMeta(ns, key, timeout); });
	}
	Error EnumMeta(std::string_view ns, std::vector<std::string>& keys, std::chrono::milliseconds timeout) {
		return execute([this, ns, &keys, timeout] { return enumMeta(ns, keys, timeout); });
	}
	Error Select(std::string_view query, QueryResultsWrapper& result, std::chrono::milliseconds timeout);
	Error EnumNamespaces(std::vector<NamespaceDef>& defs, EnumNamespacesOpts opts, std::chrono::milliseconds timeout) {
		return execute([this, &defs, &opts, timeout] { return enumNamespaces(defs, opts, timeout); });
	}
	Error FetchResults(QueryResultsWrapper& result);
	Error StartTransaction(std::string_view ns, TransactionWrapper& transactionWrapper,
						   std::chrono::milliseconds timeout);
	typename DBT::ItemT NewItem(typename DBT::TransactionT& transaction) {
		typename DBT::ItemT item;
		execute([this, &transaction, &item] {
			item = newItem(transaction);
			return item.Status();
		});
		return item;
	}
	Error Modify(typename DBT::TransactionT& transaction, typename DBT::ItemT&& item, ItemModifyMode mode) {
		return execute([this, &transaction, &item, mode] { return modify(transaction, std::move(item), mode); });
	}
	Error CommitTransaction(typename DBT::TransactionT& transaction, size_t& count, std::chrono::milliseconds timeout) {
		return execute([this, &transaction, &count, timeout] { return commitTransaction(transaction, count, timeout); });
	}
	Error RollbackTransaction(typename DBT::TransactionT& transaction, std::chrono::milliseconds timeout) {
		return execute([this, &transaction, timeout] { return rollbackTransaction(transaction, timeout); });
	}
	Error SelectQuery(const Query& query, QueryResultsWrapper& result, std::chrono::milliseconds timeout) {
		return execute([this, &query, &result, timeout] { return selectQuery(query, result, timeout); });
	}
	Error DeleteQuery(const Query& query, size_t& count, std::chrono::milliseconds timeout) {
		return execute([this, &query, &count, timeout] { return deleteQuery(query, count, timeout); });
	}
	Error UpdateQuery(const Query& query, QueryResultsWrapper& result, std::chrono::milliseconds timeout) {
		return execute([this, &query, &result, timeout] { return updateQuery(query, result, timeout); });
	}

private:
	Error execute(std::function<Error()> f);

	Error connect(const std::string& dsn, std::chrono::milliseconds timeout);
	Error openNamespace(std::string_view ns, std::chrono::milliseconds timeout);
	Error closeNamespace(std::string_view ns, std::chrono::milliseconds timeout);
	Error dropNamespace(std::string_view ns, std::chrono::milliseconds timeout);
	Error addIndex(std::string_view ns, const IndexDef& idx, std::chrono::milliseconds timeout);
	Error updateIndex(std::string_view ns, const IndexDef& idx, std::chrono::milliseconds timeout);
	Error dropIndex(std::string_view ns, const IndexDef& idx, std::chrono::milliseconds timeout);
	typename DBT::ItemT newItem(std::string_view ns, std::chrono::milliseconds timeout);
	Error insert(std::string_view ns, typename DBT::ItemT& item, std::chrono::milliseconds timeout);
	Error upsert(std::string_view ns, typename DBT::ItemT& item, std::chrono::milliseconds timeout);
	Error update(std::string_view ns, typename DBT::ItemT& item, std::chrono::milliseconds timeout);
	Error deleteItem(std::string_view ns, typename DBT::ItemT& item, std::chrono::milliseconds timeout);
	Error putMeta(std::string_view ns, const std::string& key, std::string_view data, std::chrono::milliseconds timeout);
	Error getMeta(std::string_view ns, const std::string& key, std::string& data, std::chrono::milliseconds timeout);
	Error deleteMeta(std::string_view ns, const std::string& key, std::chrono::milliseconds timeout);
	Error enumMeta(std::string_view ns, std::vector<std::string>& keys, std::chrono::milliseconds timeout);
	Error select(std::string_view query, typename DBT::QueryResultsT& result, std::chrono::milliseconds timeout);
	Error enumNamespaces(std::vector<NamespaceDef>& defs, EnumNamespacesOpts opts, std::chrono::milliseconds timeout);
	typename DBT::TransactionT startTransaction(std::string_view ns, std::chrono::milliseconds timeout);
	typename DBT::ItemT newItem(typename DBT::TransactionT& transaction) { return transaction.NewItem(); }
	Error modify(typename DBT::TransactionT& transaction, typename DBT::ItemT&& item, ItemModifyMode mode);
	Error commitTransaction(typename DBT::TransactionT& transaction, size_t& count, std::chrono::milliseconds timeout);
	Error rollbackTransaction(typename DBT::TransactionT& transaction, std::chrono::milliseconds timeout);
	Error selectQuery(const Query& query, QueryResultsWrapper& result, std::chrono::milliseconds timeout);
	Error deleteQuery(const Query& query, size_t& count, std::chrono::milliseconds timeout);
	Error updateQuery(const Query& query, QueryResultsWrapper& result, std::chrono::milliseconds timeout);
	Error stop();

	DBT db_;
	std::thread executionThr_;
	reindexer::net::ev::dynamic_loop loop_;
	ICommand* curCmd_{nullptr};
	reindexer::net::ev::async cmdAsync_;
	std::mutex mtx_;
	std::condition_variable condVar_;
	reindexer::coroutine::channel<bool> stopCh_;
};

}  // namespace pyreindexer

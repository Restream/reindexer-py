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

	Error Connect(const std::string& dsn) { return execute([this, &dsn] { return connect(dsn); }); }
	Error OpenNamespace(std::string_view ns) { return execute([this, &ns] { return openNamespace(ns); }); }
	Error CloseNamespace(std::string_view ns) { return execute([this, ns] { return closeNamespace(ns); }); }
	Error DropNamespace(std::string_view ns) { return execute([this, ns] { return dropNamespace(ns); }); }
	Error AddIndex(std::string_view ns, const IndexDef& idx) {
		return execute([this, ns, &idx] { return addIndex(ns, idx); });
	}
	Error UpdateIndex(std::string_view ns, const IndexDef& idx) {
		return execute([this, ns, &idx] { return updateIndex(ns, idx); });
	}
	Error DropIndex(std::string_view ns, const IndexDef& idx) {
		return execute([this, ns, &idx] { return dropIndex(ns, idx); });
	}
	typename DBT::ItemT NewItem(std::string_view ns) {
		typename DBT::ItemT item;
		execute([this, ns, &item] {
			item = newItem(ns);
			return item.Status();
		});
		return item;
	}
	Error Insert(std::string_view ns, typename DBT::ItemT& item) {
		return execute([this, ns, &item] { return insert(ns, item); });
	}
	Error Upsert(std::string_view ns, typename DBT::ItemT& item) {
		return execute([this, ns, &item] { return upsert(ns, item); });
	}
	Error Update(std::string_view ns, typename DBT::ItemT& item) {
		return execute([this, ns, &item] { return update(ns, item); });
	}
	Error Delete(std::string_view ns, typename DBT::ItemT& item) {
		return execute([this, ns, &item] { return deleteItem(ns, item); });
	}
	Error PutMeta(std::string_view ns, const std::string& key, std::string_view data) {
		return execute([this, ns, &key, data] { return putMeta(ns, key, data); });
	}
	Error GetMeta(std::string_view ns, const std::string& key, std::string& data) {
		return execute([this, ns, &key, &data] { return getMeta(ns, key, data); });
	}
	Error DeleteMeta(std::string_view ns, const std::string& key) {
		return execute([this, ns, &key] { return deleteMeta(ns, key); });
	}
	Error EnumMeta(std::string_view ns, std::vector<std::string>& keys) {
		return execute([this, ns, &keys] { return enumMeta(ns, keys); });
	}
	Error Select(const std::string& query, QueryResultsWrapper& result);
	Error EnumNamespaces(std::vector<NamespaceDef>& defs, EnumNamespacesOpts opts) {
		return execute([this, &defs, &opts] { return enumNamespaces(defs, opts); });
	}
	Error FetchResults(QueryResultsWrapper& result);
	Error StartTransaction(std::string_view ns, TransactionWrapper& transactionWrapper);
	typename DBT::ItemT NewItem(typename DBT::TransactionT& tr) {
		typename DBT::ItemT item;
		execute([this, &tr, &item] {
			item = newItem(tr);
			return item.Status();
		});
		return item;
	}
	Error Modify(typename DBT::TransactionT& tr, typename DBT::ItemT&& item, ItemModifyMode mode) {
		return execute([this, &tr, &item, mode] { return modify(tr, std::move(item), mode); });
	}
	Error CommitTransaction(typename DBT::TransactionT& tr, size_t& count) {
		return execute([this, &tr, &count] { return commitTransaction(tr, count); });
	}
	Error RollbackTransaction(typename DBT::TransactionT& tr) {
		return execute([this, &tr] { return rollbackTransaction(tr); });
	}
	Error SelectQuery(const Query& query, QueryResultsWrapper& result) {
		return execute([this, &query, &result] { return selectQuery(query, result); });
	}
	Error DeleteQuery(const Query& query, size_t& count) {
		return execute([this, &query, &count] { return deleteQuery(query, count); });
	}
	Error UpdateQuery(const Query& query, QueryResultsWrapper& result) {
		return execute([this, &query, &result] { return updateQuery(query, result); });
	}

private:
	Error execute(std::function<Error()> f);

	Error connect(const std::string& dsn);
	Error openNamespace(std::string_view ns) { return db_.OpenNamespace(ns); }
	Error closeNamespace(std::string_view ns) { return db_.CloseNamespace(ns); }
	Error dropNamespace(std::string_view ns) { return db_.DropNamespace(ns); }
	Error addIndex(std::string_view ns, const IndexDef& idx) { return db_.AddIndex(ns, idx); }
	Error updateIndex(std::string_view ns, const IndexDef& idx) { return db_.UpdateIndex(ns, idx); }
	Error dropIndex(std::string_view ns, const IndexDef& idx) { return db_.DropIndex(ns, idx); }
	typename DBT::ItemT newItem(std::string_view ns) { return db_.NewItem(ns); }
	Error insert(std::string_view ns, typename DBT::ItemT& item) { return db_.Insert(ns, item); }
	Error upsert(std::string_view ns, typename DBT::ItemT& item) { return db_.Upsert(ns, item); }
	Error update(std::string_view ns, typename DBT::ItemT& item) { return db_.Update(ns, item); }
	Error deleteItem(std::string_view ns, typename DBT::ItemT& item) { return db_.Delete(ns, item); }
	Error putMeta(std::string_view ns, const std::string& key, std::string_view data) {
		return db_.PutMeta(ns, key, data);
	}
	Error getMeta(std::string_view ns, const std::string& key, std::string& data) {
		return db_.GetMeta(ns, key, data);
	}
	Error deleteMeta(std::string_view ns, const std::string& key) { return db_.DeleteMeta(ns, key); }
	Error enumMeta(std::string_view ns, std::vector<std::string>& keys) { return db_.EnumMeta(ns, keys); }
	Error select(const std::string& query, typename DBT::QueryResultsT& result) { return db_.Select(query, result); }
	Error enumNamespaces(std::vector<NamespaceDef>& defs, EnumNamespacesOpts opts) {
		return db_.EnumNamespaces(defs, opts);
	}
	typename DBT::TransactionT startTransaction(std::string_view ns) { return db_.NewTransaction(ns); }
	typename DBT::ItemT newItem(typename DBT::TransactionT& tr) { return tr.NewItem(); }
	Error modify(typename DBT::TransactionT& tr, typename DBT::ItemT&& item, ItemModifyMode mode);
	Error commitTransaction(typename DBT::TransactionT& transaction, size_t& count);
	Error rollbackTransaction(typename DBT::TransactionT& tr) { return db_.RollBackTransaction(tr); }
	Error selectQuery(const Query& query, QueryResultsWrapper& result);
	Error deleteQuery(const Query& query, size_t& count);
	Error updateQuery(const Query& query, QueryResultsWrapper& result);
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

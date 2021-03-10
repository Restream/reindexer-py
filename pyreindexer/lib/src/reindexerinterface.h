#pragma once

#include <condition_variable>
#include <thread>
#include "core/indexdef.h"
#include "core/namespacedef.h"
#include "coroutine/channel.h"
#include "net/ev/ev.h"
#include "tools/errors.h"

namespace pyreindexer {

using reindexer::Error;
using reindexer::net::ev::dynamic_loop;
using reindexer::IndexDef;
using reindexer::NamespaceDef;
using reindexer::EnumNamespacesOpts;
using std::string_view;

class QueryResultsWrapper;

struct ICommand {
	virtual Error Status() const = 0;
	virtual void Execute() = 0;
	virtual bool IsExecuted() const = 0;

	virtual ~ICommand() = default;
};

class GenericCommand : public ICommand {
public:
	using CallableT = std::function<Error()>;

	GenericCommand(CallableT command) : command_(std::move(command)) {}

	Error Status() const override final { return err_; }
	void Execute() override final {
		err_ = command_();
		executed_.store(true, std::memory_order_release);
	}
	bool IsExecuted() const override final { return executed_.load(std::memory_order_acquire); }

private:
	CallableT command_;
	Error err_;
	std::atomic<bool> executed_ = {false};
};

template <typename DBT>
class ReindexerInterface {
	using namespace reindexer;
public:
	ReindexerInterface();
	~ReindexerInterface();

	Error Connect(const std::string& dsn) {
		return execute([this, &dsn] { return connect(dsn); });
	}
	Error OpenNamespace(string_view ns) {
		return execute([this, &ns] { return openNamespace(ns); });
	}
	Error CloseNamespace(string_view ns) {
		return execute([this, &ns] { return closeNamespace(ns); });
	}
	Error DropNamespace(string_view ns) {
		return execute([this, &ns] { return dropNamespace(ns); });
	}
	Error AddIndex(string_view ns, const IndexDef& idx) {
		return execute([this, &ns, &idx] { return addIndex(ns, idx); });
	}
	Error UpdateIndex(string_view ns, const IndexDef& idx) {
		return execute([this, &ns, &idx] { return updateIndex(ns, idx); });
	}
	Error DropIndex(string_view ns, const IndexDef& idx) {
		return execute([this, &ns, &idx] { return dropIndex(ns, idx); });
	}
	typename DBT::ItemT NewItem(string_view ns) {
		typename DBT::ItemT item;
		execute([this, &ns, &item] {
			item = newItem(ns);
			return item.Status();
		});
		return item;
	}
	Error Insert(string_view ns, typename DBT::ItemT& item) {
		return execute([this, &ns, &item] { return insert(ns, item); });
	}
	Error Upsert(string_view ns, typename DBT::ItemT& item) {
		return execute([this, &ns, &item] { return upsert(ns, item); });
	}
	Error Update(string_view ns, typename DBT::ItemT& item) {
		return execute([this, &ns, &item] { return update(ns, item); });
	}
	Error Delete(string_view ns, typename DBT::ItemT& item) {
		return execute([this, &ns, &item] { return deleteImpl(ns, item); });
	}
	Error Commit(string_view ns) {
		return execute([this, &ns] { return commit(ns); });
	}
	Error PutMeta(string_view ns, const std::string& key, string_view data) {
		return execute([this, &ns, &key, &data] { return putMeta(ns, key, data); });
	}
	Error GetMeta(string_view ns, const std::string& key, std::string& data) {
		return execute([this, &ns, &key, &data] { return getMeta(ns, key, data); });
	}
	Error EnumMeta(string_view ns, std::vector<std::string>& keys) {
		return execute([this, &ns, &keys] { return enumMeta(ns, keys); });
	}
	Error Select(string_view query, QueryResultsWrapper& result);
	Error EnumNamespaces(std::vector<NamespaceDef>& defs, EnumNamespacesOpts opts) {
		return execute([this, &defs, &opts] { return enumNamespaces(defs, opts); });
	}
	Error FetchResults(QueryResultsWrapper& result);

private:
	Error execute(std::function<Error()> f);

	Error connect(const std::string& dsn);
	Error openNamespace(string_view ns) { return db_.OpenNamespace(ns); }
	Error closeNamespace(string_view ns) { return db_.CloseNamespace(ns); }
	Error dropNamespace(string_view ns) { return db_.DropNamespace(ns); }
	Error addIndex(string_view ns, const IndexDef& idx) { return db_.AddIndex(ns, idx); }
	Error updateIndex(string_view ns, const IndexDef& idx) { return db_.UpdateIndex(ns, idx); }
	Error dropIndex(string_view ns, const IndexDef& idx) { return db_.DropIndex(ns, idx); }
	typename DBT::ItemT newItem(string_view ns) { return db_.NewItem(ns); }
	Error insert(string_view ns, typename DBT::ItemT& item) { return db_.Insert(ns, item); }
	Error upsert(string_view ns, typename DBT::ItemT& item) { return db_.Upsert(ns, item); }
	Error update(string_view ns, typename DBT::ItemT& item) { return db_.Update(ns, item); }
	Error deleteImpl(string_view ns, typename DBT::ItemT& item) { return db_.Delete(ns, item); }
	Error commit(string_view ns) { return db_.Commit(ns); }
	Error putMeta(string_view ns, const std::string& key, string_view data) { return db_.PutMeta(ns, key, data); }
	Error getMeta(string_view ns, const std::string& key, std::string& data) { return db_.GetMeta(ns, key, data); }
	Error enumMeta(string_view ns, std::vector<std::string>& keys) { return db_.EnumMeta(ns, keys); }
	Error select(string_view query, typename DBT::QueryResultsT& result) { return db_.Select(query, result); }
	Error enumNamespaces(std::vector<NamespaceDef>& defs, EnumNamespacesOpts opts) { return db_.EnumNamespaces(defs, opts); }
	Error stop();

	DBT db_;
	std::thread executionThr_;
	dynamic_loop loop_;
	ICommand* curCmd_ = nullptr;
	reindexer::net::ev::async cmdAsync_;
	std::mutex mtx_;
	std::condition_variable condVar_;
	reindexer::coroutine::channel<bool> stopCh_;
};

}  // namespace pyreindexer

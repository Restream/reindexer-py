#include "reindexerinterface.h"
#include "client/cororeindexer.h"
#include "core/reindexer.h"
#include "core/type_consts.h"
#include "queryresults_wrapper.h"
#include "transaction_wrapper.h"

namespace pyreindexer {
namespace {
	const int QRESULTS_FLAGS = kResultsJson | kResultsWithJoined;
}

class ICommand {
public:
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
	std::atomic_bool executed_{false};
};

namespace {
reindexer::client::ReindexerConfig makeClientConfig(const ReindexerConfig& cfg) {
	reindexer::client::ReindexerConfig config;
	config.FetchAmount = cfg.fetchAmount;
	config.ReconnectAttempts = cfg.reconnectAttempts;
	// config.NetTimeout = cfg.netTimeout; // ToDo after migrate on v.4
	config.EnableCompression = cfg.enableCompression;
	config.RequestDedicatedThread = cfg.requestDedicatedThread;
	config.AppName = cfg.appName;
	//config.SyncRxCoroCount = cfg.syncRxCoroCount; // ToDo after migrate on v.4
	return config;
}
} // namespace

template <>
ReindexerInterface<reindexer::Reindexer>::ReindexerInterface(const ReindexerConfig& cfg)
	: db_(reindexer::ReindexerConfig().WithUpdatesSize(cfg.maxReplUpdatesSize)
									  .WithAllocatorCacheLimits(cfg.allocatorCacheLimit, cfg.allocatorCachePart))
{ }

template <>
ReindexerInterface<reindexer::client::CoroReindexer>::ReindexerInterface(const ReindexerConfig& cfg)
	: db_(makeClientConfig(cfg)) {
	std::atomic_bool running{false};
	executionThr_ = std::thread([this, &running] {
		cmdAsync_.set(loop_);
		cmdAsync_.set([this](reindexer::net::ev::async&) {
			loop_.spawn([this] {
				std::unique_lock<std::mutex> lck(mtx_);
				if (curCmd_) {
					auto cmd = curCmd_;
					curCmd_ = nullptr;
					lck.unlock();
					loop_.spawn([this, cmd] {
						cmd->Execute();
						std::unique_lock<std::mutex> lck(mtx_);
						condVar_.notify_all();
					});
				}
			});
		});
		cmdAsync_.start();

		loop_.spawn([this] {
			// This coroutine should prevent loop from stopping for core::Reindexer
			stopCh_.pop();
		});

		running = true;
		loop_.run();
	});
	while (!running) {
		std::this_thread::yield();
	}
}

template <typename DBT>
ReindexerInterface<DBT>::~ReindexerInterface() {
	if (executionThr_.joinable()) {
		execute([this] { return stop(); });
		executionThr_.join();
	}
}

template <typename DBT>
Error ReindexerInterface<DBT>::Select(std::string_view query, QueryResultsWrapper& result,
									  std::chrono::milliseconds timeout) {
	return execute([this, query, &result, timeout] {
		typename DBT::QueryResultsT qres(QRESULTS_FLAGS);
		auto res = select(query, qres, timeout);
		result.Wrap(std::move(qres));
		return res;
	});
}

template <typename DBT>
Error ReindexerInterface<DBT>::FetchResults(QueryResultsWrapper& result) {
	return execute([&result] {
		result.FetchResults();
		return Error();
	});
}

template <typename DBT>
Error ReindexerInterface<DBT>::StartTransaction(std::string_view ns, TransactionWrapper& transactionWrapper,
												std::chrono::milliseconds timeout) {
	return execute([this, ns, &transactionWrapper, timeout] {
		auto transaction = startTransaction(ns, timeout);
		auto error = transaction.Status();
		transactionWrapper.Wrap(std::move(transaction));
		return error;
	});
}

template <typename DBT>
Error ReindexerInterface<DBT>::openNamespace(std::string_view ns, std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).OpenNamespace({ns.data(), ns.size()});
}

template <typename DBT>
Error ReindexerInterface<DBT>::closeNamespace(std::string_view ns, std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).CloseNamespace({ns.data(), ns.size()});
}

template <typename DBT>
Error ReindexerInterface<DBT>::dropNamespace(std::string_view ns, std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).DropNamespace(ns);
}

template <typename DBT>
Error ReindexerInterface<DBT>::addIndex(std::string_view ns, const IndexDef& idx, std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).AddIndex(ns, idx);
}

template <typename DBT>
Error ReindexerInterface<DBT>::updateIndex(std::string_view ns, const IndexDef& idx,
										   std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).UpdateIndex(ns, idx);
}

template <typename DBT>
Error ReindexerInterface<DBT>::dropIndex(std::string_view ns, const IndexDef& idx, std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).DropIndex({ns.data(), ns.size()}, idx);
}

template <typename DBT>
typename DBT::ItemT ReindexerInterface<DBT>::newItem(std::string_view ns, std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).NewItem({ns.data(), ns.size()});
}

template <typename DBT>
Error ReindexerInterface<DBT>::insert(std::string_view ns, typename DBT::ItemT& item,
									  std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).Insert({ns.data(), ns.size()}, item);
}

template <typename DBT>
Error ReindexerInterface<DBT>::upsert(std::string_view ns, typename DBT::ItemT& item,
									  std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).Upsert({ns.data(), ns.size()}, item);
}

template <typename DBT>
Error ReindexerInterface<DBT>::update(std::string_view ns, typename DBT::ItemT& item,
									  std::chrono::milliseconds timeout)
 {
	return db_.WithTimeout(timeout).Update({ns.data(), ns.size()}, item);
}

template <typename DBT>
Error ReindexerInterface<DBT>::deleteItem(std::string_view ns, typename DBT::ItemT& item,
										  std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).Delete({ns.data(), ns.size()}, item);
}

template <typename DBT>
Error ReindexerInterface<DBT>::putMeta(std::string_view ns, const std::string& key, std::string_view data,
									   std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).PutMeta(ns, key, data);
}

template <typename DBT>
Error ReindexerInterface<DBT>::getMeta(std::string_view ns, const std::string& key, std::string& data,
									   std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).GetMeta(ns, key, data);
}

template <typename DBT>
Error ReindexerInterface<DBT>::deleteMeta(std::string_view ns, const std::string& key,
										  std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).DeleteMeta(ns, key);
}

template <typename DBT>
Error ReindexerInterface<DBT>::enumMeta(std::string_view ns, std::vector<std::string>& keys,
										std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).EnumMeta(ns, keys);
}

template <typename DBT>
Error ReindexerInterface<DBT>::select(std::string_view query, typename DBT::QueryResultsT& result,
									  std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).Select(query, result);
}

template <typename DBT>
Error ReindexerInterface<DBT>::enumNamespaces(std::vector<NamespaceDef>& defs, EnumNamespacesOpts opts,
											  std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).EnumNamespaces(defs, opts);
}

template <>
Error ReindexerInterface<reindexer::Reindexer>::modify(reindexer::Transaction& transaction,
			reindexer::Item&& item, ItemModifyMode mode) {
	transaction.Modify(std::move(item), mode);
	return {};
}
template <>
Error ReindexerInterface<reindexer::client::CoroReindexer>::modify(reindexer::client::CoroTransaction& transaction,
			reindexer::client::Item&& item, ItemModifyMode mode) {
	return transaction.Modify(std::move(item), mode);
}

template <typename DBT>
typename DBT::TransactionT ReindexerInterface<DBT>::startTransaction(std::string_view ns,
																	 std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).NewTransaction(ns);
}

template <typename DBT>
Error ReindexerInterface<DBT>::commitTransaction(typename DBT::TransactionT& transaction, size_t& count,
												 std::chrono::milliseconds timeout) {
	typename DBT::QueryResultsT qres(QRESULTS_FLAGS);
	auto err = db_.WithTimeout(timeout).CommitTransaction(transaction, qres);
	count = qres.Count();
	return err;
}

template <typename DBT>
Error ReindexerInterface<DBT>::rollbackTransaction(typename DBT::TransactionT& transaction,
												   std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).RollBackTransaction(transaction);
}

template <typename DBT>
Error ReindexerInterface<DBT>::selectQuery(const Query& query, QueryResultsWrapper& result,
										   std::chrono::milliseconds timeout) {
	typename DBT::QueryResultsT qres(QRESULTS_FLAGS);
	auto err = db_.WithTimeout(timeout).Select(query, qres);
	result.Wrap(std::move(qres));
	return err;
}

template <typename DBT>
Error ReindexerInterface<DBT>::deleteQuery(const Query& query, size_t& count, std::chrono::milliseconds timeout) {
	typename DBT::QueryResultsT qres;
	auto err = db_.WithTimeout(timeout).Delete(query, qres);
	count = qres.Count();
	return err;
}

template <typename DBT>
Error ReindexerInterface<DBT>::updateQuery(const Query& query, QueryResultsWrapper& result,
										   std::chrono::milliseconds timeout) {
	typename DBT::QueryResultsT qres(QRESULTS_FLAGS);
	auto err = db_.WithTimeout(timeout).Update(query, qres);
	result.Wrap(std::move(qres));
	return err;
}

template <>
Error ReindexerInterface<reindexer::Reindexer>::execute(std::function<Error()> f) {
	return f();
}

template <>
Error ReindexerInterface<reindexer::client::CoroReindexer>::execute(std::function<Error()> f) {
	std::unique_lock<std::mutex> lck_(mtx_);
	assert(curCmd_ == nullptr);
	GenericCommand cmd(std::move(f));
	curCmd_ = &cmd;
	cmdAsync_.send();
	condVar_.wait(lck_, [&cmd] { return cmd.IsExecuted(); });
	return cmd.Status();
}

template <>
Error ReindexerInterface<reindexer::Reindexer>::connect(const std::string& dsn, std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).Connect(dsn);
}

template <>
Error ReindexerInterface<reindexer::client::CoroReindexer>::connect(
		const std::string& dsn, std::chrono::milliseconds timeout) {
	return db_.WithTimeout(timeout).Connect(dsn, loop_, reindexer::client::ConnectOpts().CreateDBIfMissing());
}

template <>
Error ReindexerInterface<reindexer::Reindexer>::stop() {
	return {};
}

template <>
Error ReindexerInterface<reindexer::client::CoroReindexer>::stop() {
	db_.Stop();
	stopCh_.close();
	return {};
}

#ifdef PYREINDEXER_CPROTO
template class ReindexerInterface<reindexer::client::CoroReindexer>;
#else
template class ReindexerInterface<reindexer::Reindexer>;
#endif

}  // namespace pyreindexer

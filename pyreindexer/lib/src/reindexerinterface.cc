#include "reindexerinterface.h"
#include "client/cororeindexer.h"
#include "core/reindexer.h"
#include "queryresults_wrapper.h"

namespace pyreindexer {

template <>
ReindexerInterface<reindexer::Reindexer>::ReindexerInterface() {}

template <>
ReindexerInterface<reindexer::client::CoroReindexer>::ReindexerInterface() {
	std::atomic<bool> running{false};
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
Error ReindexerInterface<DBT>::Select(const std::string &query, QueryResultsWrapper& result) {
	return execute([this, &query, &result] {
		auto res = select(query, result.qresPtr);
		result.db_ = this;
		result.iterInit();
		return res;
	});
}

template <typename DBT>
Error ReindexerInterface<DBT>::FetchResults(QueryResultsWrapper& result) {
	return execute([this, &result] {
		++(result.itPtr);
		if (result.itPtr == result.qresPtr.end()) {
			result.iterInit();
		}
		return errOK;
	});
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
Error ReindexerInterface<reindexer::Reindexer>::connect(const std::string& dsn) {
	return db_.Connect(dsn);
}

template <>
Error ReindexerInterface<reindexer::client::CoroReindexer>::connect(const std::string& dsn) {
	return db_.Connect(dsn, loop_, reindexer::client::ConnectOpts().CreateDBIfMissing());
}

template <>
Error ReindexerInterface<reindexer::Reindexer>::stop() {
	return errOK;
}

template <>
Error ReindexerInterface<reindexer::client::CoroReindexer>::stop() {
	db_.Stop();
	stopCh_.close();
	return errOK;
}

#ifdef PYREINDEXER_CPROTO
template class ReindexerInterface<reindexer::client::CoroReindexer>;
#else
template class ReindexerInterface<reindexer::Reindexer>;
#endif

}  // namespace pyreindexer

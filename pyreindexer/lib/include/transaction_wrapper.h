#pragma once

#include "reindexerinterface.h"
#include "core/query/query.h"

#ifdef PYREINDEXER_CPROTO
#include "client/cororeindexer.h"
#else
#include "core/reindexer.h"
#endif

namespace pyreindexer {

#ifdef PYREINDEXER_CPROTO
using DBInterface = ReindexerInterface<reindexer::client::CoroReindexer>;
using TransactionT = reindexer::client::CoroTransaction;
using QueryResultsT = reindexer::client::CoroQueryResults;
using ItemT = reindexer::client::Item;
#else
using DBInterface = ReindexerInterface<reindexer::Reindexer>;
using TransactionT = reindexer::Transaction;
using QueryResultsT = reindexer::QueryResults;
using ItemT = reindexer::Item;
#endif

class TransactionWrapper {
public:
	TransactionWrapper(DBInterface* db) : db_{db} {
		assert(db_);
	}

	void Wrap(TransactionT&& transaction) {
		transaction_ = std::move(transaction);
	}

	Error Start(std::string_view ns, std::chrono::milliseconds timeout) {
		return db_->StartTransaction(ns, *this, timeout);
	}

	ItemT NewItem() {
		assert(transaction_.has_value());
		return db_->NewItem(*transaction_);
	}

	Error Modify(ItemT&& item, ItemModifyMode mode) {
		assert(transaction_.has_value());
		return db_->Modify(*transaction_, std::move(item), mode);
	}

	Error Commit(size_t& count, std::chrono::milliseconds timeout) {
		assert(transaction_.has_value());
		return db_->CommitTransaction(*transaction_, count, timeout);
	}

	Error Rollback(std::chrono::milliseconds timeout) {
		assert(transaction_.has_value());
		return db_->RollbackTransaction(*transaction_, timeout);
	}

private:
	DBInterface* db_{nullptr};
	std::optional<TransactionT> transaction_;
};

}  // namespace pyreindexer

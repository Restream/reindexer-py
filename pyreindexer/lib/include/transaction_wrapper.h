#pragma once

#include "reindexerinterface.h"

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
		wrap_ = true;
	}

	Error Start(std::string_view ns) {
		return db_->StartTransaction(ns, *this);
	}

	ItemT NewItem() {
		assert(wrap_);
		return db_->NewItem(transaction_);
	}

	Error Modify(ItemT&& item, ItemModifyMode mode) {
		assert(wrap_);
		return db_->Modify(transaction_, std::move(item), mode);
	}

	Error Commit(size_t& count) {
		assert(wrap_);
		return db_->CommitTransaction(transaction_, count);
	}

	Error Rollback() {
		assert(wrap_);
		return db_->RollbackTransaction(transaction_);
	}

private:
	DBInterface* db_{nullptr};
	TransactionT transaction_;
	bool wrap_{false};
};

}  // namespace pyreindexer

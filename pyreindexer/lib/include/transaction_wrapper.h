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
using ItemT = reindexer::client::Item;
#else
using DBInterface = ReindexerInterface<reindexer::Reindexer>;
using TransactionT = reindexer::Transaction;
using ItemT = reindexer::Item;
#endif

class TransactionWrapper {
public:
	TransactionWrapper(DBInterface* db) : db_{db} {
		assert(db_);
	}

	void Init(std::string_view ns, TransactionT&& transaction) {
		transaction_ = std::move(transaction);
		ns_ = ns;
	}

	Error Start(std::string_view ns) {
		assert(!ns_.empty());
		return db_->StartTransaction(ns, *this);
	}

	Error Commit() {
		assert(!ns_.empty());
		return db_->CommitTransaction(transaction_);
	}

	Error Rollback() {
		assert(!ns_.empty());
		return db_->RollbackTransaction(transaction_);
	}

	Error Modify(ItemT&& item, ItemModifyMode mode) {
		assert(!ns_.empty());
		return db_->Modify(transaction_, std::move(item), mode);
	}

	ItemT NewItem() {
		assert(!ns_.empty());
		return db_->NewItem(ns_);
	}

private:
	DBInterface* db_ = nullptr;
	TransactionT transaction_;
	std::string ns_;
};

}  // namespace pyreindexer

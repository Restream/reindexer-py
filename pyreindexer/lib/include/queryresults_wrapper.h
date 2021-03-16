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
using QueryResultsT = reindexer::client::CoroQueryResults;
#else
using DBInterface = ReindexerInterface<reindexer::Reindexer>;
using QueryResultsT = reindexer::QueryResults;
#endif

class QueryResultsWrapper {
public:
	size_t Count() const { return qresPtr.Count(); }
	void GetItemJSON(reindexer::WrSerializer& wrser, bool withHdrLen) { itPtr.GetJSON(wrser, withHdrLen); }
	void Next() {
		assert(db_);
		db_->FetchResults(*this);
	}

private:
	friend DBInterface;

	void iterInit() { itPtr = qresPtr.begin(); }

	DBInterface* db_ = nullptr;
	QueryResultsT qresPtr;
	QueryResultsT::Iterator itPtr;
};

}  // namespace pyreindexer

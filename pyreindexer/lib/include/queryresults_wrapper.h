#pragma once

#include "core/type_consts.h"
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
	QueryResultsWrapper(DBInterface* db) : db_{db}, qres_{kResultsJson} {
		assert(db_);
	}

	void Wrap(QueryResultsT&& qres) {
		qres_ = std::move(qres);
		it_ = qres_.begin();
		wrap_ = true;
	}

	Error Select(const std::string& query) {
		return db_->Select(query, *this);
	}

	size_t Count() const {
		assert(wrap_);
		return qres_.Count();
	}

	void GetItemJSON(reindexer::WrSerializer& wrser, bool withHdrLen) {
		assert(wrap_);
		it_.GetJSON(wrser, withHdrLen);
	}

	void Next() {
		assert(wrap_);
		db_->FetchResults(*this);
	}

	void FetchResults() {
		assert(wrap_);
		// when results are fetched iterator closes and frees a memory of results buffer of Reindexer
		++it_;
	}

	const std::vector<reindexer::AggregationResult>& GetAggregationResults() & { return qres_.GetAggregationResults(); }
	const std::vector<reindexer::AggregationResult>& GetAggregationResults() && = delete;

private:
	DBInterface* db_{nullptr};
	QueryResultsT qres_;
	QueryResultsT::Iterator it_;
	bool wrap_{false};
};

}  // namespace pyreindexer

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
	}

	Error Select(const std::string& query) {
		return db_->Select(query, *this);
	}

	size_t Count() const { return qres_.Count(); }

	void GetItemJSON(reindexer::WrSerializer& wrser, bool withHdrLen) { it_.GetJSON(wrser, withHdrLen); }

	void Next() {
		db_->FetchResults(*this);
	}

	void FetchResults() {
		++it_;
		if (it_ == qres_.end()) {
			it_ = qres_.begin();
		}
	}

	const std::vector<reindexer::AggregationResult>& GetAggregationResults() const& { return qres_.GetAggregationResults(); }
	const std::vector<reindexer::AggregationResult>& GetAggregationResults() const&& = delete;

private:
	DBInterface* db_{nullptr};
	QueryResultsT qres_;
	QueryResultsT::Iterator it_;
};

}  // namespace pyreindexer

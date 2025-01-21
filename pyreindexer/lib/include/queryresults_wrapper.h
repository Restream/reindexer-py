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
	QueryResultsWrapper(DBInterface* db) : db_{db} {
		assert(db_);
	}

	void Wrap(QueryResultsT&& qres) {
		qres_ = std::move(qres);
		it_ = qres_->begin();
	}

	Error Select(std::string_view query, std::chrono::milliseconds timeout) {
		return db_->Select(query, *this, timeout);
	}

	Error Status() {
		assert(qres_.has_value());
		return (it_ == qres_->end()) ? Error() : it_.Status();
	}

	size_t Count() const noexcept {
		assert(qres_.has_value());
		return qres_->Count();
	}

	size_t TotalCount() const noexcept {
		assert(qres_.has_value());
		return qres_->TotalCount();
	}

	void GetItemJSON(reindexer::WrSerializer& wrser, bool withHdrLen) {
		assert(qres_.has_value());
		it_.GetJSON(wrser, withHdrLen);
	}

	void Next() {
		assert(qres_.has_value());
		db_->FetchResults(*this);
	}

	void FetchResults() {
		assert(qres_.has_value());
		// when results are fetched iterator closes and frees memory of results buffer of Reindexer
		++it_;
	}

	const std::string& GetExplainResults() & noexcept {
		assert(qres_.has_value());
		return qres_->GetExplainResults();
	}
	const std::string& GetExplainResults() && = delete;

	const std::vector<reindexer::AggregationResult>& GetAggregationResults() &
	{
		assert(qres_.has_value());
		return qres_->GetAggregationResults();
	}
	const std::vector<reindexer::AggregationResult>& GetAggregationResults() && = delete;

private:
	DBInterface* db_{nullptr};
	std::optional<QueryResultsT> qres_;
	QueryResultsT::Iterator it_;
};

}  // namespace pyreindexer

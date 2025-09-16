#pragma once

#include "core/type_consts.h"
#include "reindexerinterface.h"

#ifdef PYREINDEXER_CPROTO
#include "client/reindexer.h"
#else
#include "core/reindexer.h"
#endif

namespace pyreindexer {

#ifdef PYREINDEXER_CPROTO
using DBInterface = ReindexerInterface<reindexer::client::Reindexer>;
using QueryResultsT = reindexer::client::QueryResults;
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
		res_.emplace(std::move(qres));
	}

	Error ExecSQL(std::string_view query, std::chrono::milliseconds timeout) {
		return db_->ExecSQL(query, *this, timeout);
	}

	Error Status() {
		assert(res_.has_value());
		return (res_->it == res_->qres.end()) ? Error() : res_->it.Status();
	}

	size_t Count() const noexcept {
		assert(res_.has_value());
		return res_->qres.Count();
	}

	size_t TotalCount() const noexcept {
		assert(res_.has_value());
		return res_->qres.TotalCount();
	}

	Error GetItemJSON(reindexer::WrSerializer& wrser, bool withHdrLen) {
		assert(res_.has_value());
		return res_->it.GetJSON(wrser, withHdrLen);
	}

	Error Next() {
		assert(res_.has_value());
		return db_->FetchResults(*this);
	}

	void FetchResults() {
		assert(res_.has_value());
		// when results are fetched iterator closes and frees memory of results buffer of Reindexer
		++(*res_).it;
	}

	const std::string& GetExplainResults() & {
		assert(res_.has_value());
		return res_->qres.GetExplainResults();
	}
	const std::string& GetExplainResults() && = delete;

	const std::vector<reindexer::AggregationResult>& GetAggregationResults() &
	{
		assert(res_.has_value());
		return res_->qres.GetAggregationResults();
	}
	const std::vector<reindexer::AggregationResult>& GetAggregationResults() && = delete;

private:
	struct Results {
		Results() = delete;
		Results(QueryResultsT&& qr) noexcept : qres(std::move(qr)), it(qres.begin())
		{ }
		Results(const Results&) noexcept = delete;
		Results(Results&&) noexcept = delete;
		Results& operator=(Results&&) noexcept = delete;
		Results& operator=(const Results&) noexcept = delete;

		QueryResultsT qres;
		QueryResultsT::Iterator it;
	};
	DBInterface* db_{nullptr};
	std::optional<Results> res_;
};

}  // namespace pyreindexer

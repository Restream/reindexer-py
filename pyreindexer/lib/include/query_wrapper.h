#pragma once

#include <deque>

#include "core/type_consts.h"
#include "estl/h_vector.h"
#include "tools/serializer.h"
#include "tools/errors.h"
#ifdef PYREINDEXER_CPROTO
#include "client/cororeindexer.h"
#else
#include "core/reindexer.h"
#endif

#include "reindexerinterface.h"

namespace pyreindexer {

#ifdef PYREINDEXER_CPROTO
using DBInterface = ReindexerInterface<reindexer::client::CoroReindexer>;
#else
using DBInterface = ReindexerInterface<reindexer::Reindexer>;
#endif

class QueryResultsWrapper;

class QueryWrapper {
public:
	QueryWrapper(DBInterface* db, std::string_view ns);

	void Where(std::string_view index, CondType condition, const reindexer::VariantArray& keys);
	void WhereSubQuery(QueryWrapper& query, CondType condition, const reindexer::VariantArray& keys);
	void WhereFieldSubQuery(std::string_view index, CondType condition, QueryWrapper& query);
	void WhereUUID(std::string_view index, CondType condition, const reindexer::h_vector<std::string, 2>& keys);

	void WhereBetweenFields(std::string_view firstField, CondType condition, std::string_view secondField);

	reindexer::Error OpenBracket();
	reindexer::Error CloseBracket();

	void DWithin(std::string_view index, double x, double y, double distance);

	void Aggregate(std::string_view index, AggType type);
	void Aggregation(const reindexer::h_vector<std::string, 2>& fields);
	void AggregationSort(std::string_view field, bool desc);

	void Sort(std::string_view index, bool desc, const reindexer::VariantArray& sortValues);

	void LogOp(OpType op);

	void Total(CalcTotalMode mode);

	void AddValue(QueryItemType type, unsigned value);

	void Modifier(QueryItemType type);

	reindexer::Error SelectQuery(std::unique_ptr<QueryResultsWrapper>& qr, std::chrono::milliseconds timeout);
	reindexer::Error UpdateQuery(std::unique_ptr<QueryResultsWrapper>& qr, std::chrono::milliseconds timeout);
	reindexer::Error DeleteQuery(size_t& count, std::chrono::milliseconds timeout);

	enum class IsExpression { Yes, No };
	void Set(std::string_view field, const reindexer::VariantArray& values, IsExpression isExpression);
	void SetObject(std::string_view field, const reindexer::h_vector<std::string, 2>& values);

	void Drop(std::string_view field);

	void Join(JoinType type, QueryWrapper* joinQuery);
	void Merge(QueryWrapper* mergeQuery);

	reindexer::Error On(std::string_view joinField, CondType condition, std::string_view joinIndex);

	void SelectFilter(const reindexer::h_vector<std::string, 2>& fields);

	void AddFunctions(const reindexer::h_vector<std::string, 2>& functions);
	void AddEqualPosition(const reindexer::h_vector<std::string, 2>& equalPositions);

private:
	reindexer::Error buildQuery(reindexer::Query& query);
	void addJoinQueries(const reindexer::h_vector<QueryWrapper*, 1>& queries, reindexer::WrSerializer& buffer) const;
	void putKeys(const reindexer::VariantArray& keys);

	DBInterface* db_{nullptr};
	reindexer::WrSerializer ser_;

	OpType nextOperation_{OpType::OpAnd};
	unsigned queriesCount_{0};
	std::deque<uint32_t> openedBrackets_;
	JoinType joinType_{JoinType::LeftJoin};
	reindexer::h_vector<QueryWrapper*, 1> joinQueries_;
	reindexer::h_vector<QueryWrapper*, 1> mergedQueries_;
};

}  // namespace pyreindexer

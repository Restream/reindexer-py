#pragma once

#include <deque>

#include "core/type_consts.h"
#include "tools/serializer.h"
#include "tools/errors.h"
#ifdef PYREINDEXER_CPROTO
#include "client/cororeindexer.h"
#else
#include "core/reindexer.h"
#endif

#include "reindexerinterface.h"
#include "queryresults_wrapper.h"

namespace pyreindexer {

#ifdef PYREINDEXER_CPROTO
using DBInterface = ReindexerInterface<reindexer::client::CoroReindexer>;
#else
using DBInterface = ReindexerInterface<reindexer::Reindexer>;
#endif

class QueryWrapper {
public:
	QueryWrapper(DBInterface* db, std::string_view ns);

	void Where(std::string_view index, CondType condition, const std::vector<reindexer::Variant>& keys);
	void WhereQuery(QueryWrapper& query, CondType condition, const std::vector<reindexer::Variant>& keys);
	void WhereComposite(std::string_view index, CondType condition, QueryWrapper& query);
	void WhereUUID(std::string_view index, CondType condition, const std::vector<std::string>& keys);

	void WhereBetweenFields(std::string_view firstField, CondType condition, std::string_view secondField);

	reindexer::Error OpenBracket();
	reindexer::Error CloseBracket();

	void DWithin(std::string_view index, double x, double y, double distance);

	void Aggregate(std::string_view index, AggType type);
	void Aggregation(const std::vector<std::string>& fields);
	void AggregationSort(std::string_view field, bool desc);

	void Sort(std::string_view index, bool desc, const std::vector<reindexer::Variant>& keys);

	void LogOp(OpType op);

	void Total(std::string_view totalName, CalcTotalMode mode);

	void AddValue(QueryItemType type, unsigned value);

	void Strict(StrictMode mode);

	void Modifier(QueryItemType type);

	enum class ExecuteType { Select, Update };
	reindexer::Error ExecuteQuery(ExecuteType type, QueryResultsWrapper& qr);
	reindexer::Error DeleteQuery(size_t& count);

	enum class IsExpression { Yes, No };
	void Set(std::string_view field, const std::vector<reindexer::Variant>& values, IsExpression isExpression);
	void SetObject(std::string_view field, const std::vector<std::string>& values);

	void Drop(std::string_view field);

	void Join(JoinType type, unsigned joinQueryIndex, QueryWrapper* joinQuery);
	void Merge(QueryWrapper* mergeQuery);

	reindexer::Error On(std::string_view joinField, CondType condition, std::string_view joinIndex);

	void SelectFilter(const std::vector<std::string>& fields);

	void AddFunctions(const std::vector<std::string>& functions);
	void AddEqualPosition(const std::vector<std::string>& equalPositions);

	DBInterface* GetDB() const { return db_; }

private:
	reindexer::Serializer prepareQueryData(reindexer::WrSerializer& data);
	reindexer::JoinedQuery createJoinedQuery(JoinType joinType, reindexer::WrSerializer& data);
	void addJoinQueries(const std::vector<QueryWrapper*>& joinQueries, reindexer::Query& query);
	reindexer::Query prepareQuery();

	DBInterface* db_{nullptr};
	reindexer::WrSerializer ser_;

	OpType nextOperation_{OpType::OpAnd};
	unsigned queriesCount_{0};
	std::deque<uint32_t> openedBrackets_;
	std::string totalName_; // ToDo now not used
	JoinType joinType_{JoinType::LeftJoin};
	std::vector<QueryWrapper*> joinQueries_;
	std::vector<QueryWrapper*> mergedQueries_;
};

}  // namespace pyreindexer

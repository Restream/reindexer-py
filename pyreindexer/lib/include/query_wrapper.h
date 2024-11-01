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

namespace pyreindexer {

#ifdef PYREINDEXER_CPROTO
using DBInterface = ReindexerInterface<reindexer::client::CoroReindexer>;
#else
using DBInterface = ReindexerInterface<reindexer::Reindexer>;
#endif

class QueryWrapper {
public:
	QueryWrapper(DBInterface* db, std::string_view ns);

	template <typename T>
	void Where(std::string_view index, CondType condition, const std::vector<T>& keys) {
		ser_.PutVarUint(QueryItemType::QueryCondition);
		ser_.PutVString(index);
		ser_.PutVarUint(nextOperation_);
		ser_.PutVarUint(condition);

		ser_.PutVarUint(keys.size());
		for (const auto& key : keys) {
			putValue(key);
		}

		nextOperation_ = OpType::OpAnd;
		++queriesCount_;
	}
	template <typename T>
	void WhereQuery(QueryWrapper& query, CondType condition, const std::vector<T>& keys) {
		ser_.PutVarUint(QueryItemType::QuerySubQueryCondition);
		ser_.PutVarUint(nextOperation_);
		ser_.PutVString(query.ser_.Slice());
		ser_.PutVarUint(condition);

		ser_.PutVarUint(keys.size());
		for (const auto& key : keys) {
			putValue(key);
		}

		nextOperation_ = OpType::OpAnd;
		++queriesCount_;
	}
	void WhereComposite(std::string_view index, CondType condition, QueryWrapper& query);
	void WhereUUID(std::string_view index, CondType condition, const std::vector<std::string>& keys);

	void WhereBetweenFields(std::string_view firstField, CondType condition, std::string_view secondField);

	reindexer::Error OpenBracket();
	reindexer::Error CloseBracket();

	void DWithin(std::string_view index, double x, double y, double distance);

	void Aggregate(std::string_view index, AggType type);
	void Aggregation(const std::vector<std::string>& fields);
	void AggregationSort(std::string_view field, bool desc);

	template <typename T>
	void Sort(std::string_view index, bool desc, const std::vector<T>& keys) {
		ser_.PutVarUint(QueryItemType::QuerySortIndex);
		ser_.PutVString(index);
		ser_.PutVarUint(desc? 1 : 0);

		ser_.PutVarUint(keys.size());
		for (const auto& key : keys) {
			putValue(key);
		}
	}

	void LogOp(OpType op);

	void Total(std::string_view totalName, CalcTotalMode mode);

	void AddValue(QueryItemType type, unsigned value);

	void Strict(StrictMode mode);

	void Modifier(QueryItemType type);

	void SetObject(std::string_view field, const std::vector<std::string>& values, QueryItemType type) {
		ser_.PutVarUint(type);
		ser_.PutVString(field);
		if (type == QueryItemType::QueryUpdateObject) {
			ser_.PutVarUint(values.size()); // values count
		}
		if (type != QueryItemType::QueryUpdateField) {
			ser_.PutVarUint(values.size() > 1? 1 : 0); // is array flag
		}
		if (type != QueryItemType::QueryUpdateObject) {
			ser_.PutVarUint(values.size()); // values count
		}
		for (const auto& value : values) {
			ser_.PutVarUint(0); // function/value flag
			putValue(value);
		}
	}

	void Drop(std::string_view field);

	void SetExpression(std::string_view field, std::string_view value);

	reindexer::Error On(std::string_view joinField, CondType condition, std::string_view joinIndex);

	void Select(const std::vector<std::string>& fields);

	void FetchCount(int count);

	void AddFunctions(const std::vector<std::string>& functions);
	void AddEqualPosition(const std::vector<std::string>& equalPositions);

private:
	template <typename T>
	void putValue(T) {}

private:
	DBInterface* db_{nullptr}; // ToDo
	reindexer::WrSerializer ser_;

	OpType nextOperation_{OpType::OpAnd};
	unsigned queriesCount_{0};
	std::deque<uint32_t> openedBrackets_;
	std::string totalName_;
	int fetchCount_{0};
};

}  // namespace pyreindexer

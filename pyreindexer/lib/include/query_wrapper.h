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

	void WhereBetweenFields(std::string_view firstField, CondType condition, std::string_view secondField);

	reindexer::Error OpenBracket();
	reindexer::Error CloseBracket();

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

	void LogOp(OpType op);

	void Distinct(std::string_view index);

	void ReqTotal(std::string_view totalName);
	void CachedTotal(std::string_view totalName);

	void Limit(unsigned limitItems);
	void Offset(unsigned startOffset);
	void Debug(unsigned level);
	void Strict(StrictMode mode);

	void Modifier(QueryItemType type);

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
	DBInterface* db_{nullptr};
	reindexer::WrSerializer ser_;

	OpType nextOperation_{OpType::OpAnd};
	unsigned queriesCount_{0};
	std::deque<uint32_t> openedBrackets_;
	std::string totalName_;
	int fetchCount_{0};
};

}  // namespace pyreindexer

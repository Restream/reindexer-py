#pragma once

#include <deque>
#include <limits>
#include "core/type_consts.h"
#include "core/keyvalue/uuid.h"
#include "core/keyvalue/variant.h"
#include "tools/serializer.h"
#include "tools/errors.h"

namespace pyreindexer {

namespace {
    const int VALUE_INT_64 = 0;
    const int VALUE_DOUBLE = 1;
    const int VALUE_STRING = 2;
    const int VALUE_BOOL = 3;
    const int VALUE_NULL = 4;
    const int VALUE_INT = 8;
    const int VALUE_UNDEFINED = 9;
    const int VALUE_COMPOSITE = 10;
    const int VALUE_TUPLE = 11;
    const int VALUE_UUID = 12;
}

class QueryWrapper {
public:
	QueryWrapper(DBInterface* db, std::string_view ns) : db_{db} {
		assert(db_);
		ser_.PutVString(ns);
	}

	void WhereBetweenFields(std::string_view firstField, CondType condition, std::string_view secondField) {
		ser_.PutVarUint(QueryItemType::QueryBetweenFieldsCondition);
		ser_.PutVarUint(nextOperation_);
		ser_.PutVString(firstField);
		ser_.PutVarUint(condition);
		ser_.PutVString(secondField);
		nextOperation_ = OpType::OpAnd;
		++queriesCount_;
	}

	Error OpenBracket() {
		ser_.PutVarUint(QueryItemType::QueryOpenBracket);
		ser_.PutVarUint(nextOperation_);
		nextOperation_ = OpType::OpAnd;
		openedBrackets_.push_back(queriesCount_);
		++queriesCount_;
		return errOK;
	}

	Error CloseBracket() {
		if (nextOperation_ != OpType::OpAnd) {
			return Error(errLogic, "Operation before close bracket");
		}

		if (openedBrackets_.empty()) {
			return Error(errLogic, "Close bracket before open it");
		}

		ser_.PutVarUint(QueryItemType::QueryCloseBracket);
		openedBrackets_.pop_back();
		return errOK;
	}

	template <typename T> // ToDo --------------------------------------------------------------
	void Where(std::string_view index, CondType condition, const std::vector<T>& keys) {
		(void)index;
		(void)condition;
		(void)keys;
	} //---------------------------------------------------------

	void WhereUUID(std::string_view index, CondType condition, const std::vector<std::string>& keys) {
		ser_.PutVarUint(QueryItemType::QueryCondition);
		ser_.PutVString(index);
		ser_.PutVarUint(nextOperation_);
		ser_.PutVarUint(condition);
		nextOperation_ = OpType::OpAnd;
		++queriesCount_;

		ser_.PutVarUint(keys.size());
		for (const auto& key : keys) {
			try {
				auto uuid = reindexer::Uuid(key);
				ser_.PutVarUint(VALUE_UUID);
				ser_.PutUuid(uuid);
			} catch (const Error& err) {
				ser_.PutVarUint(VALUE_STRING);
				ser_.PutVString(key);
			}
		}
	}

	void LogOp(OpType op) {
		switch (op) {
			case OpType::OpAnd:
			case OpType::OpOr:
			case OpType::OpNot:
				break;
			default:
				assert(false);
		}
		nextOperation_ = op;
	}

	void Distinct(std::string_view index) {
		ser_.PutVarUint(QueryItemType::QueryAggregation);
		ser_.PutVarUint(AggType::AggDistinct);
		ser_.PutVarUint(1);
		ser_.PutVString(index);
	}

	void ReqTotal(std::string_view totalName) {
		ser_.PutVarUint(QueryItemType::QueryReqTotal);
		ser_.PutVarUint(CalcTotalMode::ModeAccurateTotal);
		if (!totalName.empty()) {
			totalName_ = totalName;
		}
	}

	void CachedTotal(std::string_view totalName) {
		ser_.PutVarUint(QueryItemType::QueryReqTotal);
		ser_.PutVarUint(CalcTotalMode::ModeCachedTotal);
		if (!totalName.empty()) {
			totalName_ = totalName;
		}
	}

	void Limit(unsigned limitItems) {
		int limit = std::min<int>(std::numeric_limits<int>::max(), limitItems);
		ser_.PutVarUint(QueryItemType::QueryLimit);
		ser_.PutVarUint(limit);
	}

	void Offset(int startOffset) {
		int offset = std::min<int>(std::numeric_limits<int>::max(), startOffset);
		ser_.PutVarUint(QueryItemType::QueryOffset);
		ser_.PutVarUint(offset);
	}

	void Debug(int level) {
		ser_.PutVarUint(QueryItemType::QueryDebugLevel);
		ser_.PutVarUint(level);
	}

	void Strict(StrictMode mode) {
		ser_.PutVarUint(QueryItemType::QueryStrictMode);
		ser_.PutVarUint(mode);
	}

	void Modifier(QueryItemType type) {
		ser_.PutVarUint(type);
	}

	void Drop(std::string_view field) {
		ser_.PutVarUint(QueryItemType::QueryDropField);
		ser_.PutVString(field);
	}

	void SetExpression(std::string_view field, std::string_view value) {
		ser_.PutVarUint(QueryItemType::QueryUpdateField);
		ser_.PutVString(field);

		ser_.PutVarUint(1); // size
		ser_.PutVarUint(1); // is expression
		ser_.PutVString(value);	// ToDo q.putValue(value);
	}

	Error On(std::string_view joinField, CondType condition, std::string_view joinIndex) {
		// ToDo
		/*if q.closed {
			q.panicTrace("query.On call on already closed query. You should create new Query")
		}
		if q.root == nil {
			panic(fmt.Errorf("Can't join on root query"))
		}*/
		ser_.PutVarUint(QueryItemType::QueryJoinOn);
		ser_.PutVarUint(nextOperation_);
		ser_.PutVarUint(condition);
		ser_.PutVString(joinField);
		ser_.PutVString(joinIndex);
		nextOperation_ = OpType::OpAnd;
		return errOK;
	}

	void Select(const std::vector<std::string>& fields) {
		for (const auto& field : fields) {
			ser_.PutVarUint(QueryItemType::QuerySelectFilter);
			ser_.PutVString(field);
		}
	}

	void FetchCount(int count) {
		fetchCount_ = count;
	}

	void AddFunctions(const std::vector<std::string>& functions) {
		for (const auto& function : functions) {
			ser_.PutVarUint(QueryItemType::QuerySelectFunction);
			ser_.PutVString(function);
		}
	}

	void AddEqualPosition(const std::vector<std::string>& equalPositions) {
		ser_.PutVarUint(QueryItemType::QueryEqualPosition);
		ser_.PutVarUint(openedBrackets_.empty()? 0 : int(openedBrackets_.back() + 1));
		ser_.PutVarUint(equalPositions.size());
		for (const auto& position : equalPositions) {
			ser_.PutVString(position);
		}
	}

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

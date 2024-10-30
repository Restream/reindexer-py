#include "query_wrapper.h"

#include <limits>

#include "core/keyvalue/uuid.h"

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

	QueryWrapper::QueryWrapper(DBInterface* db, std::string_view ns) : db_{db} {
		assert(db_);
		ser_.PutVString(ns);
	}

	void QueryWrapper::WhereBetweenFields(std::string_view firstField, CondType condition, std::string_view secondField) {
		ser_.PutVarUint(QueryItemType::QueryBetweenFieldsCondition);
		ser_.PutVarUint(nextOperation_);
		ser_.PutVString(firstField);
		ser_.PutVarUint(condition);
		ser_.PutVString(secondField);
		nextOperation_ = OpType::OpAnd;
		++queriesCount_;
	}

	Error QueryWrapper::OpenBracket() {
		ser_.PutVarUint(QueryItemType::QueryOpenBracket);
		ser_.PutVarUint(nextOperation_);
		nextOperation_ = OpType::OpAnd;
		openedBrackets_.push_back(queriesCount_);
		++queriesCount_;
		return errOK;
	}

	reindexer::Error QueryWrapper::CloseBracket() {
		if (nextOperation_ != OpType::OpAnd) {
			return reindexer::Error(errLogic, "Operation before close bracket");
		}

		if (openedBrackets_.empty()) {
			return reindexer::Error(errLogic, "Close bracket before open it");
		}

		ser_.PutVarUint(QueryItemType::QueryCloseBracket);
		openedBrackets_.pop_back();
		return errOK;
	}

	void QueryWrapper::WhereUUID(std::string_view index, CondType condition, const std::vector<std::string>& keys) {
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

	void QueryWrapper::LogOp(OpType op) {
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

	void QueryWrapper::Distinct(std::string_view index) {
		ser_.PutVarUint(QueryItemType::QueryAggregation);
		ser_.PutVarUint(AggType::AggDistinct);
		ser_.PutVarUint(1);
		ser_.PutVString(index);
	}

	void QueryWrapper::ReqTotal(std::string_view totalName) {
		ser_.PutVarUint(QueryItemType::QueryReqTotal);
		ser_.PutVarUint(CalcTotalMode::ModeAccurateTotal);
		if (!totalName.empty()) {
			totalName_ = totalName;
		}
	}

	void QueryWrapper::CachedTotal(std::string_view totalName) {
		ser_.PutVarUint(QueryItemType::QueryReqTotal);
		ser_.PutVarUint(CalcTotalMode::ModeCachedTotal);
		if (!totalName.empty()) {
			totalName_ = totalName;
		}
	}

	void QueryWrapper::Limit(unsigned limitItems) {
		ser_.PutVarUint(QueryItemType::QueryLimit);
		ser_.PutVarUint(limitItems);
	}

	void QueryWrapper::Offset(unsigned startOffset) {
		int offset = std::min<int>(std::numeric_limits<int>::max(), startOffset);
		ser_.PutVarUint(QueryItemType::QueryOffset);
		ser_.PutVarUint(offset);
	}

	void QueryWrapper::Debug(unsigned level) {
		ser_.PutVarUint(QueryItemType::QueryDebugLevel);
		ser_.PutVarUint(level);
	}

	void QueryWrapper::Strict(StrictMode mode) {
		ser_.PutVarUint(QueryItemType::QueryStrictMode);
		ser_.PutVarUint(mode);
	}

	void QueryWrapper::Modifier(QueryItemType type) {
		ser_.PutVarUint(type);
	}

	void QueryWrapper::Drop(std::string_view field) {
		ser_.PutVarUint(QueryItemType::QueryDropField);
		ser_.PutVString(field);
	}

	void QueryWrapper::SetExpression(std::string_view field, std::string_view value) {
		ser_.PutVarUint(QueryItemType::QueryUpdateField);
		ser_.PutVString(field);

		ser_.PutVarUint(1); // size
		ser_.PutVarUint(1); // is expression
		ser_.PutVString(value);	// ToDo q.putValue(value);
	}

	reindexer::Error QueryWrapper::On(std::string_view joinField, CondType condition, std::string_view joinIndex) {
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

	void QueryWrapper::Select(const std::vector<std::string>& fields) {
		for (const auto& field : fields) {
			ser_.PutVarUint(QueryItemType::QuerySelectFilter);
			ser_.PutVString(field);
		}
	}

	void QueryWrapper::FetchCount(int count) {
		fetchCount_ = count;
	}

	void QueryWrapper::AddFunctions(const std::vector<std::string>& functions) {
		for (const auto& function : functions) {
			ser_.PutVarUint(QueryItemType::QuerySelectFunction);
			ser_.PutVString(function);
		}
	}

	void QueryWrapper::AddEqualPosition(const std::vector<std::string>& equalPositions) {
		ser_.PutVarUint(QueryItemType::QueryEqualPosition);
		ser_.PutVarUint(openedBrackets_.empty()? 0 : int(openedBrackets_.back() + 1));
		ser_.PutVarUint(equalPositions.size());
		for (const auto& position : equalPositions) {
			ser_.PutVString(position);
		}
	}

	template <>
	void QueryWrapper::putValue(int8_t value) {
		ser_.PutVarUint(VALUE_INT);
		ser_.PutVarint(value);
	}
	template <>
	void QueryWrapper::putValue(uint8_t value) {
		ser_.PutVarUint(VALUE_INT);
		ser_.PutVarint(int64_t(value));
	}
	template <>
	void QueryWrapper::putValue(int16_t value) {
		ser_.PutVarUint(VALUE_INT);
		ser_.PutVarint(value);
	}
	template <>
	void QueryWrapper::putValue(uint16_t value) {
		ser_.PutVarUint(VALUE_INT);
		ser_.PutVarint(int64_t(value));
	}
	template <>
	void QueryWrapper::putValue(int32_t value) {
		ser_.PutVarUint(VALUE_INT);
		ser_.PutVarint(value);
	}
	template <>
	void QueryWrapper::putValue(uint32_t value) {
		ser_.PutVarUint(VALUE_INT);
		ser_.PutVarint(int64_t(value));
	}
	template <>
	void QueryWrapper::putValue(int64_t value) {
		ser_.PutVarUint(VALUE_INT_64);
		ser_.PutVarint(value);
	}
	template <>
	void QueryWrapper::putValue(uint64_t value) {
		ser_.PutVarUint(VALUE_INT_64);
		ser_.PutVarint(value);
	}
	template <>
	void QueryWrapper::putValue(std::string_view value) {
		ser_.PutVarUint(VALUE_STRING);
		ser_.PutVString(value);
	}
	template <>
	void QueryWrapper::putValue(bool value) {
		ser_.PutVarUint(VALUE_BOOL);
		ser_.PutBool(value);
	}
	template <>
	void QueryWrapper::putValue(double value) {
		ser_.PutVarUint(VALUE_DOUBLE);
		ser_.PutDouble(value);
	}

}  // namespace pyreindexer

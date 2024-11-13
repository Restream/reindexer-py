#include "query_wrapper.h"

#include <limits>

#include "core/query/query.h"
#include "core/keyvalue/uuid.h"

namespace pyreindexer {

namespace {
	const int VALUE_INT_64    = 0;
	const int VALUE_DOUBLE    = 1;
	const int VALUE_STRING    = 2;
	const int VALUE_BOOL      = 3;
	const int VALUE_NULL      = 4;
	const int VALUE_INT       = 8;
	const int VALUE_UNDEFINED = 9;
	const int VALUE_COMPOSITE = 10;
	const int VALUE_TUPLE     = 11;
	const int VALUE_UUID      = 12;
} // namespace

QueryWrapper::QueryWrapper(DBInterface* db, std::string_view ns) : db_{db} {
	assert(db_);
	ser_.PutVString(ns);
}

void QueryWrapper::Where(std::string_view index, CondType condition, const std::vector<reindexer::Variant>& keys) {
	ser_.PutVarUint(QueryItemType::QueryCondition);
	ser_.PutVString(index);
	ser_.PutVarUint(nextOperation_);
	ser_.PutVarUint(condition);

	ser_.PutVarUint(keys.size());
	for (const auto& key : keys) {
		ser_.PutVariant(key);
	}

	nextOperation_ = OpType::OpAnd;
	++queriesCount_;
}

void QueryWrapper::WhereQuery(QueryWrapper& query, CondType condition, const std::vector<reindexer::Variant>& keys) {
	ser_.PutVarUint(QueryItemType::QuerySubQueryCondition);
	ser_.PutVarUint(nextOperation_);
	ser_.PutVString(query.ser_.Slice());
	ser_.PutVarUint(condition);

	ser_.PutVarUint(keys.size());
	for (const auto& key : keys) {
		ser_.PutVariant(key);
	}

	nextOperation_ = OpType::OpAnd;
	++queriesCount_;
}

void QueryWrapper::WhereComposite(std::string_view index, CondType condition, QueryWrapper& query) {
	ser_.PutVarUint(QueryItemType::QueryFieldSubQueryCondition);
	ser_.PutVarUint(nextOperation_);
	ser_.PutVString(index);
	ser_.PutVarUint(condition);
	ser_.PutVString(query.ser_.Slice());

	nextOperation_ = OpType::OpAnd;
	++queriesCount_;
}

void QueryWrapper::WhereUUID(std::string_view index, CondType condition, const std::vector<std::string>& keys) {
	ser_.PutVarUint(QueryItemType::QueryCondition);
	ser_.PutVString(index);
	ser_.PutVarUint(nextOperation_);
	ser_.PutVarUint(condition);

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

	nextOperation_ = OpType::OpAnd;
	++queriesCount_;
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
	openedBrackets_.push_back(queriesCount_);

	nextOperation_ = OpType::OpAnd;
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

void QueryWrapper::DWithin(std::string_view index, double x, double y, double distance) {
	ser_.PutVarUint(QueryItemType::QueryCondition);
	ser_.PutVString(index);
	ser_.PutVarUint(nextOperation_);
	ser_.PutVarUint(CondType::CondDWithin);

	ser_.PutVarUint(3);
	ser_.PutVarUint(VALUE_DOUBLE);
	ser_.PutDouble(x);
	ser_.PutVarUint(VALUE_DOUBLE);
	ser_.PutDouble(y);
	ser_.PutVarUint(VALUE_DOUBLE);
	ser_.PutDouble(distance);

	nextOperation_ = OpType::OpAnd;
	++queriesCount_;
}

void QueryWrapper::AggregationSort(std::string_view field, bool desc) {
	ser_.PutVarUint(QueryItemType::QueryAggregationSort);
	ser_.PutVString(field);
	ser_.PutVarUint(desc? 1 : 0);
}

void QueryWrapper::Aggregate(std::string_view index, AggType type) {
	ser_.PutVarUint(QueryItemType::QueryAggregation);
	ser_.PutVarUint(type);
	ser_.PutVarUint(1);
	ser_.PutVString(index);
}

void QueryWrapper::Aggregation(const std::vector<std::string>& fields) {
	ser_.PutVarUint(QueryItemType::QueryAggregation);
	ser_.PutVarUint(AggType::AggFacet);
	ser_.PutVarUint(fields.size());
	for (const auto& field : fields) {
		ser_.PutVString(field);
	}
}

void QueryWrapper::Sort(std::string_view index, bool desc, const std::vector<reindexer::Variant>& keys) {
	ser_.PutVarUint(QueryItemType::QuerySortIndex);
	ser_.PutVString(index);
	ser_.PutVarUint(desc? 1 : 0);

	ser_.PutVarUint(keys.size());
	for (const auto& key : keys) {
		ser_.PutVariant(key);
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

void QueryWrapper::Total(std::string_view totalName, CalcTotalMode mode) {
	ser_.PutVarUint(QueryItemType::QueryReqTotal);
	ser_.PutVarUint(mode);
	if (!totalName.empty()) {
		totalName_ = totalName;
	}
}

void QueryWrapper::AddValue(QueryItemType type, unsigned value) {
	ser_.PutVarUint(type);
	ser_.PutVarUint(value);
}

void QueryWrapper::Strict(StrictMode mode) {
	ser_.PutVarUint(QueryItemType::QueryStrictMode);
	ser_.PutVarUint(mode);
}

void QueryWrapper::Modifier(QueryItemType type) {
	ser_.PutVarUint(type);
}

reindexer::Serializer QueryWrapper::prepareQueryData(reindexer::WrSerializer& data) {
	reindexer::WrSerializer buffer;
	buffer.Write(data.Slice()); // do full copy of query data
	buffer.PutVarUint(QueryItemType::QueryEnd); // close query data
	return {buffer.Buf(), buffer.Len()};
}

reindexer::JoinedQuery QueryWrapper::createJoinedQuery(JoinType joinType, reindexer::WrSerializer& data) {
	reindexer::Serializer jser = prepareQueryData(data);
	return {joinType, reindexer::Query::Deserialize(jser)};
}

void QueryWrapper::addJoinQueries(const std::vector<QueryWrapper*>& joinQueries, reindexer::Query& query) {
	for (auto joinQuery : joinQueries) {
		auto jq = createJoinedQuery(joinQuery->joinType_, joinQuery->ser_);
		query.AddJoinQuery(std::move(jq));
	}
}

reindexer::Query QueryWrapper::prepareQuery() {
	reindexer::Serializer ser = prepareQueryData(ser_);
	auto query = reindexer::Query::Deserialize(ser);

	addJoinQueries(joinQueries_, query);

	for (auto mergedQuery : mergedQueries_) {
		auto mq = createJoinedQuery(JoinType::Merge, mergedQuery->ser_);
		query.Merge(std::move(mq));

		addJoinQueries(mergedQuery->joinQueries_, mq);
	}

	return query;
}

reindexer::Error QueryWrapper::SelectQuery(QueryResultsWrapper& qr) {
	auto query = prepareQuery();
	return db_->SelectQuery(query, qr);
}

reindexer::Error QueryWrapper::DeleteQuery(size_t& count) {
	auto query = prepareQuery();
	return db_->DeleteQuery(query, count);
}

reindexer::Error QueryWrapper::UpdateQuery(QueryResultsWrapper& qr) {
	auto query = prepareQuery();
	return db_->UpdateQuery(query, qr);
}

void QueryWrapper::SetObject(std::string_view field, const std::vector<std::string>& values) {
	ser_.PutVarUint(QueryItemType::QueryUpdateObject);
	ser_.PutVString(field);
	ser_.PutVarUint(values.size()); // values count
	ser_.PutVarUint(values.size() > 1? 1 : 0); // is array flag
	for (const auto& value : values) {
		ser_.PutVarUint(0); // function/value flag
		ser_.PutVarUint(TagType::TAG_STRING); // type ID
		ser_.PutVString(value);
		break;
	}
}

void QueryWrapper::Set(std::string_view field, const std::vector<reindexer::Variant>& values) {
	ser_.PutVarUint(QueryItemType::QueryUpdateFieldV2);
	ser_.PutVString(field);
	ser_.PutVarUint(values.size() > 1? 1 : 0); // is array flag
	ser_.PutVarUint(values.size()); // values count
	for (const auto& value : values) {
		ser_.PutVarUint(0); // is expression
		ser_.PutVariant(value);
	}
}

void QueryWrapper::Drop(std::string_view field) {
	ser_.PutVarUint(QueryItemType::QueryDropField);
	ser_.PutVString(field);
}

void QueryWrapper::SetExpression(std::string_view field, std::string_view value) {
	ser_.PutVarUint(QueryItemType::QueryUpdateField);
	ser_.PutVString(field);
	ser_.PutVarUint(1); // values count
	ser_.PutVarUint(1); // is expression
	ser_.PutVariant(reindexer::Variant{value});
}

void QueryWrapper::Join(JoinType type, unsigned joinQueryIndex, QueryWrapper* joinQuery) {
	assert(joinQuery);

	joinType_ = type;
	if ((joinType_ == JoinType::InnerJoin) && (nextOperation_ == OpType::OpOr)) {
		nextOperation_ = OpType::OpAnd;
		joinType_ = JoinType::OrInnerJoin;
	}
	ser_.PutVarUint(QueryJoinCondition);
	ser_.PutVarUint(joinType_);
	ser_.PutVarUint(joinQueryIndex);

	joinQueries_.push_back(joinQuery);
}

void QueryWrapper::Merge(QueryWrapper* mergeQuery) {
	assert(mergeQuery);
	mergedQueries_.push_back(mergeQuery);
}

reindexer::Error QueryWrapper::On(std::string_view joinField, CondType condition, std::string_view joinIndex) {
	ser_.PutVarUint(QueryItemType::QueryJoinOn);
	ser_.PutVarUint(nextOperation_);
	ser_.PutVarUint(condition);
	ser_.PutVString(joinField);
	ser_.PutVString(joinIndex);

	nextOperation_ = OpType::OpAnd;

	return errOK;
}

void QueryWrapper::SelectFilter(const std::vector<std::string>& fields) {
	for (const auto& field : fields) {
		ser_.PutVarUint(QueryItemType::QuerySelectFilter);
		ser_.PutVString(field);
	}
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

}  // namespace pyreindexer

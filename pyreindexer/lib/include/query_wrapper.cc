#include "query_wrapper.h"

#include <limits>

#include "core/query/query.h"
#include "core/keyvalue/uuid.h"
#include "queryresults_wrapper.h"

namespace pyreindexer {
QueryWrapper::QueryWrapper(DBInterface* db, std::string_view ns) : db_{db} {
	assert(db_);
	ser_.PutVString(ns);
}

void QueryWrapper::Where(std::string_view index, CondType condition, const reindexer::VariantArray& keys) {
	ser_.PutVarUint(QueryItemType::QueryCondition);
	ser_.PutVString(index);
	ser_.PutVarUint(nextOperation_);
	ser_.PutVarUint(condition);
	putKeys(keys);

	nextOperation_ = OpType::OpAnd;
	++queriesCount_;
}

void QueryWrapper::WhereSubQuery(QueryWrapper& query, CondType condition, const reindexer::VariantArray& keys) {
	ser_.PutVarUint(QueryItemType::QuerySubQueryCondition);
	ser_.PutVarUint(nextOperation_);
	ser_.PutVString(query.ser_.Slice());
	ser_.PutVarUint(condition);
	putKeys(keys);

	nextOperation_ = OpType::OpAnd;
	++queriesCount_;
}

void QueryWrapper::WhereFieldSubQuery(std::string_view index, CondType condition, QueryWrapper& query) {
	ser_.PutVarUint(QueryItemType::QueryFieldSubQueryCondition);
	ser_.PutVarUint(nextOperation_);
	ser_.PutVString(index);
	ser_.PutVarUint(condition);
	ser_.PutVString(query.ser_.Slice());

	nextOperation_ = OpType::OpAnd;
	++queriesCount_;
}

void QueryWrapper::WhereUUID(std::string_view index, CondType condition,
							 const reindexer::h_vector<std::string, 2>& keys) {
	ser_.PutVarUint(QueryItemType::QueryCondition);
	ser_.PutVString(index);
	ser_.PutVarUint(nextOperation_);
	ser_.PutVarUint(condition);

	ser_.PutVarUint(keys.size());
	for (const auto& key : keys) {
		try {
			auto uuid = reindexer::Uuid(key);
			ser_.PutVariant(reindexer::Variant(uuid));
		} catch (const Error& err) {
			ser_.PutVariant(reindexer::Variant(key));
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

	return {};
}

Error QueryWrapper::CloseBracket() {
	if (nextOperation_ != OpType::OpAnd) {
		return reindexer::Error(ErrorCode::errLogic, "Operation before close bracket");
	}

	if (openedBrackets_.empty()) {
		return reindexer::Error(ErrorCode::errLogic, "Close bracket before open it");
	}

	ser_.PutVarUint(QueryItemType::QueryCloseBracket);
	openedBrackets_.pop_back();

	return {};
}

void QueryWrapper::DWithin(std::string_view index, double x, double y, double distance) {
	ser_.PutVarUint(QueryItemType::QueryCondition);
	ser_.PutVString(index);
	ser_.PutVarUint(nextOperation_);
	ser_.PutVarUint(CondType::CondDWithin);

	ser_.PutVarUint(3);
	ser_.PutVariant(reindexer::Variant(x));
	ser_.PutVariant(reindexer::Variant(y));
	ser_.PutVariant(reindexer::Variant(distance));

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

void QueryWrapper::Aggregation(const reindexer::h_vector<std::string, 2>& fields) {
	ser_.PutVarUint(QueryItemType::QueryAggregation);
	ser_.PutVarUint(AggType::AggFacet);
	ser_.PutVarUint(fields.size());
	for (const auto& field : fields) {
		ser_.PutVString(field);
	}
}

void QueryWrapper::Sort(std::string_view index, bool desc, const reindexer::VariantArray& sortValues) {
	ser_.PutVarUint(QueryItemType::QuerySortIndex);
	ser_.PutVString(index);
	ser_.PutVarUint(desc? 1 : 0);
	putKeys(sortValues);
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

void QueryWrapper::Total(CalcTotalMode mode) {
	ser_.PutVarUint(QueryItemType::QueryReqTotal);
	ser_.PutVarUint(mode);
}

void QueryWrapper::AddValue(QueryItemType type, unsigned value) {
	ser_.PutVarUint(type);
	ser_.PutVarUint(value);
}

void QueryWrapper::Modifier(QueryItemType type) {
	ser_.PutVarUint(type);
}

namespace {
void serializeQuery(reindexer::WrSerializer& data, reindexer::WrSerializer& buffer) {
	buffer.Write(data.Slice()); // do full copy of query data
	buffer.PutVarUint(QueryItemType::QueryEnd); // close query data
}

void serializeJoinQuery(JoinType type, reindexer::WrSerializer& data, reindexer::WrSerializer& buffer) {
	buffer.PutVarUint(type);
	serializeQuery(data, buffer);
}
} // namespace

void QueryWrapper::addJoinQueries(const reindexer::h_vector<QueryWrapper*, 1>& queries, reindexer::WrSerializer& buffer)
 const {
	for (auto query : queries) {
		serializeJoinQuery(query->joinType_, query->ser_, buffer);
	}
}

reindexer::Error QueryWrapper::buildQuery(reindexer::Query& query) {
	reindexer::Error error = errOK;
	try {
		// current query (root)
		reindexer::WrSerializer buffer;
		serializeQuery(ser_, buffer);

		addJoinQueries(joinQueries_, buffer);

		for (auto mergedQuery : mergedQueries_) {
			serializeJoinQuery(JoinType::Merge, mergedQuery->ser_, buffer);

			addJoinQueries(mergedQuery->joinQueries_, buffer);
		}

		reindexer::Serializer fullQueryData{buffer.Buf(), buffer.Len()};
		query = reindexer::Query::Deserialize(fullQueryData);
	} catch (const reindexer::Error& err) {
		error = err;
	} catch (const std::exception& ex) {
		error = reindexer::Error(ErrorCode::errQueryExec, ex.what());
	} catch (...) {
		error = reindexer::Error(ErrorCode::errQueryExec, "Internal error");
	}

	return error;
}

reindexer::Error QueryWrapper::SelectQuery(std::unique_ptr<QueryResultsWrapper>& qr,
										   std::chrono::milliseconds timeout) {
	reindexer::Query query;
	auto err = buildQuery(query);
	if (!err.ok()) {
		return err;
	}

	if (query.IsWALQuery()) {
		return reindexer::Error(ErrorCode::errQueryExec, "WAL queries are not supported");
	}

	qr = std::make_unique<QueryResultsWrapper>(db_);
	return db_->SelectQuery(query, *qr, timeout);
}

reindexer::Error QueryWrapper::UpdateQuery(std::unique_ptr<QueryResultsWrapper>& qr,
										   std::chrono::milliseconds timeout) {
	reindexer::Query query;
	auto err = buildQuery(query);
	if (!err.ok()) {
		return err;
	}
	qr = std::make_unique<QueryResultsWrapper>(db_);
	return db_->UpdateQuery(query, *qr, timeout);
}

reindexer::Error QueryWrapper::DeleteQuery(size_t& count, std::chrono::milliseconds timeout) {
	reindexer::Query query;
	auto err = buildQuery(query);
	if (!err.ok()) {
		return err;
	}
	return db_->DeleteQuery(query, count, timeout);
}

void QueryWrapper::Set(std::string_view field, const reindexer::VariantArray& values,
					   IsExpression isExpression) {
	ser_.PutVarUint(QueryItemType::QueryUpdateFieldV2);
	ser_.PutVString(field);
	ser_.PutVarUint(values.size() > 1? 1 : 0); // is array flag
	ser_.PutVarUint(values.size()); // values count
	for (const auto& value : values) {
		ser_.PutVarUint(isExpression == IsExpression::Yes? 1 : 0); // is expression
		ser_.PutVariant(value);
	}
}

void QueryWrapper::SetObject(std::string_view field, const reindexer::h_vector<std::string, 2>& values) {
	ser_.PutVarUint(QueryItemType::QueryUpdateObject);
	ser_.PutVString(field);
	ser_.PutVarUint(values.size()); // values count
	ser_.PutVarUint(values.size() > 1? 1 : 0); // is array flag
	for (const auto& value : values) {
		ser_.PutVarUint(0); // function/value flag
		ser_.PutVariant(reindexer::Variant(value));
		break;
	}
}

void QueryWrapper::Drop(std::string_view field) {
	ser_.PutVarUint(QueryItemType::QueryDropField);
	ser_.PutVString(field);
}

void QueryWrapper::Join(JoinType type, QueryWrapper* joinQuery) {
	assert(joinQuery);

	joinType_ = type;
	if ((joinType_ == JoinType::InnerJoin) && (nextOperation_ == OpType::OpOr)) {
		nextOperation_ = OpType::OpAnd;
		joinType_ = JoinType::OrInnerJoin;
	}

	if (joinType_ != JoinType::LeftJoin) {
		ser_.PutVarUint(QueryJoinCondition);
		ser_.PutVarUint(joinType_);
		ser_.PutVarUint(joinQueries_.size());
	}

	joinQuery->joinType_ = joinType_;
	joinQueries_.push_back(joinQuery);
}

void QueryWrapper::Merge(QueryWrapper* mergeQuery) {
	assert(mergeQuery);
	mergedQueries_.push_back(mergeQuery);
}

Error QueryWrapper::On(std::string_view joinField, CondType condition, std::string_view joinIndex) {
	ser_.PutVarUint(QueryItemType::QueryJoinOn);
	ser_.PutVarUint(nextOperation_);
	ser_.PutVarUint(condition);
	ser_.PutVString(joinField);
	ser_.PutVString(joinIndex);

	nextOperation_ = OpType::OpAnd;

	return {};
}

void QueryWrapper::SelectFilter(const reindexer::h_vector<std::string, 2>& fields) {
	for (const auto& field : fields) {
		ser_.PutVarUint(QueryItemType::QuerySelectFilter);
		ser_.PutVString(field);
	}
}

void QueryWrapper::AddFunctions(const reindexer::h_vector<std::string, 2>& functions) {
	for (const auto& function : functions) {
		ser_.PutVarUint(QueryItemType::QuerySelectFunction);
		ser_.PutVString(function);
	}
}

void QueryWrapper::AddEqualPosition(const reindexer::h_vector<std::string, 2>& equalPositions) {
	ser_.PutVarUint(QueryItemType::QueryEqualPosition);
	ser_.PutVarUint(openedBrackets_.empty()? 0 : int(openedBrackets_.back() + 1));
	ser_.PutVarUint(equalPositions.size());
	for (const auto& position : equalPositions) {
		ser_.PutVString(position);
	}
}

void QueryWrapper::putKeys(const reindexer::VariantArray& keys) {
	ser_.PutVarUint(keys.size());
	for (const auto& key : keys) {
		ser_.PutVariant(key);
	}
}
}  // namespace pyreindexer

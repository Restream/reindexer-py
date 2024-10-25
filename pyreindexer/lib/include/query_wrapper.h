#pragma once

#include "core/type_consts.h"
#include "core/query/query.h"
#include "core/keyvalue/uuid.h"

namespace pyreindexer {

enum class LogOpType {
	And = 1,
	Or = 2,
	Not = 3
};

class QueryWrapper {
public:
	QueryWrapper(DBInterface* db, std::string_view ns) : db_{db}, query_(ns) {
		assert(db_);
	}

	void WhereBetweenFields(std::string_view firstField, CondType condition, std::string_view secondField) {
		query_ = std::move(query_.WhereBetweenFields(firstField, condition, secondField));
	}

	void OpenBracket() {
		query_ = std::move(query_.OpenBracket());
	}

	void CloseBracket() {
		query_ = std::move(query_.CloseBracket());
	}

	template <typename T>
	void Where(std::string_view index, CondType condition, const std::vector<T>& keys) {
		query_ = std::move(query_.Where(index, condition, keys));
	}

	Error WhereUUID(std::string_view index, CondType condition, const std::vector<std::string>& keys) {
		try {
			for (const auto& key : keys) {
				auto uuid = reindexer::Uuid(key);
				(void)uuid; // check format only
			}
		} catch (const Error& err) {
			return err;
		}

		query_ = std::move(query_.Where(index, condition, keys));
		return errOK;
	}

	void LogOp(LogOpType op) {
		switch (op) {
			case LogOpType::And:
				query_ = std::move(query_.And());
				break;
			case LogOpType::Or:
				query_ = std::move(query_.Or());
				break;
			case LogOpType::Not:
				query_ = std::move(query_.Not());
				break;
			default:
				assert(false);
		}
	}

	void Distinct(const std::string& index) {
		query_ = std::move(query_.Distinct(index));
	}

	void ReqTotal() {
		query_ = std::move(query_.ReqTotal());
	}

	void CachedTotal() {
		query_ = std::move(query_.CachedTotal());
	}

	void Limit(unsigned limitItems) {
		query_ = std::move(query_.Limit(limitItems));
	}

	void Offset(int startOffset) {
		query_ = std::move(query_.Offset(startOffset));
	}

	void Debug(int level) {
		query_ = std::move(query_.Debug(level));
	}

	void Strict(StrictMode mode) {
		query_ = std::move(query_.Strict(mode));
	}

	void Explain() {
		constexpr static bool on = true;
		query_ = std::move(query_.Explain(on));
	}

private:
	DBInterface* db_{nullptr};
	reindexer::Query query_;
};

}  // namespace pyreindexer

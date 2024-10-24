#pragma once

#include "core/type_consts.h"
#include "core/query/query.h"
#include "core/keyvalue/uuid.h"

namespace pyreindexer {

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

//	template <typename T>
//	void Where(std::string&& index, CondType condition, const std::vector<T>& keys) {
//		query_ = std::move(query_.Where<std::string, T>(std::move(index), condition, keys));
//	}
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

private:
	DBInterface* db_{nullptr};
	reindexer::Query query_;
};

}  // namespace pyreindexer

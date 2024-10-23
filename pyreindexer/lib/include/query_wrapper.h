#pragma once

#include "core/query/query.h"

namespace pyreindexer {

class QueryWrapper {
public:
	QueryWrapper(DBInterface* db, std::string_view ns) : db_{db} {
		assert(db_);
		query_ = std::make_unique<reindexer::Query>(ns);
	}

private:
	DBInterface* db_{nullptr};
	std::unique_ptr<reindexer::Query> query_;
};

}  // namespace pyreindexer

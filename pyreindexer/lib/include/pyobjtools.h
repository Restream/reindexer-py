#pragma once

#include <Python.h>
#include <vector>
//#include "estl/span.h"
#include "core/keyvalue/variant.h"
//#include "tools/serializer.h"

namespace pyreindexer {

std::vector<std::string> ParseListToStrVec(PyObject** list);
std::vector<reindexer::Variant> ParseListToVec(PyObject** list);

void PyObjectToJson(PyObject** dict, reindexer::WrSerializer& wrSer);
PyObject* PyObjectFromJson(reindexer::span<char> json);

}  // namespace pyreindexer

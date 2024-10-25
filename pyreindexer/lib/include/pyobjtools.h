#pragma once

#include <Python.h>
#include <vector>
#include "estl/span.h"
#include "vendor/gason/gason.h"
#include "tools/serializer.h"

namespace pyreindexer {

std::vector<std::string> ParseListToStrVec(PyObject** dict);

void PyObjectToJson(PyObject** dict, reindexer::WrSerializer& wrSer);
PyObject* PyObjectFromJson(reindexer::span<char> json);

}  // namespace pyreindexer

#pragma once

#include <Python.h>
#include <vector>
#include "core/keyvalue/variant.h"

namespace pyreindexer {

std::vector<std::string> ParseStrListToStrVec(PyObject** list);
std::vector<reindexer::Variant> ParseListToVec(PyObject** list);

void PyObjectToJson(PyObject** obj, reindexer::WrSerializer& wrSer);
std::vector<std::string> PyObjectToJson(PyObject** obj);
PyObject* PyObjectFromJson(reindexer::span<char> json);

}  // namespace pyreindexer

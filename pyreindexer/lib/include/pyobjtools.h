#pragma once

#include <Python.h>
#include <vector>
#include "core/keyvalue/variant.h"
#include "estl/h_vector.h"

namespace pyreindexer {

reindexer::h_vector<std::string, 2> ParseStrListToStrVec(PyObject** list);
reindexer::VariantArray ParseListToVec(PyObject** list);

void PyObjectToJson(PyObject** obj, reindexer::WrSerializer& wrSer);
reindexer::h_vector<std::string, 2> PyObjectToJson(PyObject** obj);
PyObject* PyObjectFromJson(reindexer::span<char> json);

}  // namespace pyreindexer

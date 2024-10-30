#pragma once

#include <Python.h>
#include <vector>
//#include "estl/span.h"
#include "core/keyvalue/variant.h"
//#include "tools/serializer.h"

namespace pyreindexer {

std::vector<std::string> ParseListToStrVec(PyObject** list);
std::vector<bool> ParseListToBoolVec(PyObject** list);
std::vector<double> ParseListToDoubleVec(PyObject** list);
std::vector<reindexer::Variant> ParseListToVec(PyObject** list);

template <typename T>
std::vector<T> ParseListToIntVec(PyObject** list) {
	std::vector<T> result;

	Py_ssize_t sz = PyList_Size(*list);
	result.reserve(sz);
	for (Py_ssize_t i = 0; i < sz; i++) {
		PyObject* item = PyList_GetItem(*list, i);

		if (!PyLong_Check(item)) {
			throw reindexer::Error(errParseJson, std::string("Integer expected, got ") + Py_TYPE(item)->tp_name);
		}

		long v = PyLong_AsLong(item);
		result.push_back(T(v));
	}

	return result;
}

void PyObjectToJson(PyObject** dict, reindexer::WrSerializer& wrSer);
PyObject* PyObjectFromJson(reindexer::span<char> json);

}  // namespace pyreindexer

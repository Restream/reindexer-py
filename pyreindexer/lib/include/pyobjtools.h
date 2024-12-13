#pragma once

#include <Python.h>
#include "core/keyvalue/variant.h"
#include "estl/h_vector.h"

namespace pyreindexer {

template <typename T>
using HVectorT = reindexer::h_vector<T, 2>;

template <template <typename...> class VectorT = HVectorT>
VectorT<std::string> ParseStrListToStrVec(PyObject** list) {
	VectorT<std::string> result;

	Py_ssize_t sz = PyList_Size(*list);
	result.reserve(sz);
	for (Py_ssize_t i = 0; i < sz; i++) {
		PyObject* item = PyList_GetItem(*list, i);

		if (!PyUnicode_Check(item)) {
			throw reindexer::Error(ErrorCode::errParseJson,
									std::string("String expected, got ") + Py_TYPE(item)->tp_name);
		}

		result.emplace_back(PyUnicode_AsUTF8(item));
	}

	return result;
}

reindexer::VariantArray ParseListToVec(PyObject** list);

void PyObjectToJson(PyObject** obj, reindexer::WrSerializer& wrSer);
reindexer::h_vector<std::string, 2> PyObjectToJson(PyObject** obj);
PyObject* PyObjectFromJson(reindexer::span<char> json);

}  // namespace pyreindexer

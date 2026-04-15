#pragma once

#include <Python.h>
#include <span>
#include "core/keyvalue/variant.h"
#include "estl/h_vector.h"

namespace pyreindexer {

struct PyUnicodeUTF8 {
	PyObject* objBytes = nullptr;
	const char* objStr = nullptr;

	explicit PyUnicodeUTF8(PyObject* obj) {
#if !defined(Py_LIMITED_API)
		objStr = PyUnicode_AsUTF8(obj);
#else
		objBytes = PyUnicode_AsUTF8String(obj);
		if (objBytes) {
			objStr = PyBytes_AsString(objBytes);
		}
#endif
	}

	~PyUnicodeUTF8() { Py_XDECREF(objBytes); }

	operator const char*() const noexcept { return objStr; }
	operator std::string_view() const noexcept { return objStr ? std::string_view(objStr) : std::string_view(); }

	PyUnicodeUTF8(const PyUnicodeUTF8&) = delete;
	PyUnicodeUTF8& operator=(const PyUnicodeUTF8&) = delete;
};

inline const char* py_get_type_name(PyObject* obj) {
#if defined(Py_LIMITED_API)
	#if PY_VERSION_HEX >= 0x030B0000
		return PyType_GetName(Py_TYPE(obj));
	#else
		return "<unknown type>";
	#endif
#else
	return Py_TYPE(obj)->tp_name;
#endif
}

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
									std::string("String expected, got ") + py_get_type_name(item));
		}
		result.emplace_back(PyUnicodeUTF8(item));
	}

	return result;
}

reindexer::VariantArray ParseListToVec(PyObject** list);

void PyObjectToJson(PyObject** obj, reindexer::WrSerializer& wrSer);
reindexer::h_vector<std::string, 2> PyObjectToJson(PyObject** obj);
PyObject* PyObjectFromJson(std::span<char> json);

}  // namespace pyreindexer

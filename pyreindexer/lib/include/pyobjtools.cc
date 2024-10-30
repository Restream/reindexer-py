#include "pyobjtools.h"

//#include <cmath>
#include "tools/serializer.h"
#include "vendor/gason/gason.h"

namespace pyreindexer {

void pyValueSerialize(PyObject** value, reindexer::WrSerializer& wrSer);

void pyListSerialize(PyObject** list, reindexer::WrSerializer& wrSer) {
	if (!PyList_Check(*list)) {
		throw reindexer::Error(errParseJson, std::string("List expected, got ") + Py_TYPE(*list)->tp_name);
	}

	wrSer << '[';

	Py_ssize_t sz = PyList_Size(*list);
	for (Py_ssize_t i = 0; i < sz; ++i) {
		if (i > 0) {
			wrSer << ',';
		}

		PyObject* value = PyList_GetItem(*list, i);

		pyValueSerialize(&value, wrSer);
	}

	wrSer << ']';
}

void pyDictSerialize(PyObject** dict, reindexer::WrSerializer& wrSer) {
	if (!PyDict_Check(*dict)) {
		throw reindexer::Error(errParseJson, std::string("Dictionary expected, got ") + Py_TYPE(*dict)->tp_name);
	}

	wrSer << '{';

	Py_ssize_t sz = PyDict_Size(*dict);
	if (sz) {
		PyObject *key = nullptr, *value = nullptr;
		Py_ssize_t pos = 0;

		while (PyDict_Next(*dict, &pos, &key, &value)) {
			if (pos > 1) {
				wrSer << ',';
			}

			const char* k = PyUnicode_AsUTF8(key);
			wrSer.PrintJsonString(k);
			wrSer << ':';

			pyValueSerialize(&value, wrSer);
		}
	}

	wrSer << '}';
}

void pyValueSerialize(PyObject** value, reindexer::WrSerializer& wrSer) {
	if (*value == Py_None) {
		wrSer << "null";
	} else if (PyBool_Check(*value)) {
		bool v = PyLong_AsLong(*value) != 0;
		wrSer << v;
	} else if (PyFloat_Check(*value)) {
		double v = PyFloat_AsDouble(*value);
		double intpart;
		if (std::modf(v, &intpart) == 0.0) {
			wrSer << int64_t(v);
		} else {
			wrSer << v;
		}
	} else if (PyLong_Check(*value)) {
		long v = PyLong_AsLong(*value);
		wrSer << v;
	} else if (PyUnicode_Check(*value)) {
		const char* v = PyUnicode_AsUTF8(*value);
		wrSer.PrintJsonString(v);
	} else if (PyList_Check(*value)) {
		pyListSerialize(value, wrSer);
	} else if (PyDict_Check(*value)) {
		pyDictSerialize(value, wrSer);
	} else {
		throw reindexer::Error(errParseJson, std::string("Unable to parse value of type ") + Py_TYPE(*value)->tp_name);
	}
}

void PyObjectToJson(PyObject** obj, reindexer::WrSerializer& wrSer) {
	if (PyDict_Check(*obj)) {
		pyDictSerialize(obj, wrSer);
	} else if (PyList_Check(*obj) ) {
		pyListSerialize(obj, wrSer);
	} else {
		throw reindexer::Error(errParseJson,
							   std::string("PyObject must be a dictionary or a list for JSON serializing, got ") + Py_TYPE(*obj)->tp_name);
	}
}

std::vector<std::string> ParseListToStrVec(PyObject** list) {
	std::vector<std::string> result;

	Py_ssize_t sz = PyList_Size(*list);
	result.reserve(sz);
	for (Py_ssize_t i = 0; i < sz; i++) {
		PyObject* item = PyList_GetItem(*list, i);

		if (!PyUnicode_Check(item)) {
			throw reindexer::Error(errParseJson, std::string("String expected, got ") + Py_TYPE(item)->tp_name);
		}

		result.push_back(PyUnicode_AsUTF8(item));
	}

	return result;
}

reindexer::Variant convert(PyObject** value) {
	if (PyFloat_Check(*value)) {
		double v = PyFloat_AsDouble(*value);
		double intpart = 0.0;
		if (std::modf(v, &intpart) == 0.0) {
			return reindexer::Variant(int64_t(v));
		} else {
			return reindexer::Variant(v);
		}
	} else if (PyBool_Check(*value)) {
		return reindexer::Variant(PyLong_AsLong(*value) != 0);
	} else if (PyLong_Check(*value)) {
		return reindexer::Variant(int64_t(PyLong_AsLong(*value)));
	} else if (PyUnicode_Check(*value)) {
		return reindexer::Variant(std::string_view(PyUnicode_AsUTF8(*value)));
	} else {
		throw reindexer::Error(errParseJson, std::string("Unexpected type, got ") + Py_TYPE(*value)->tp_name);
	}
	return {};
}

std::vector<reindexer::Variant> ParseListToVec(PyObject** list) {
	std::vector<reindexer::Variant> result;

	Py_ssize_t sz = PyList_Size(*list);
	result.reserve(sz);
	for (Py_ssize_t i = 0; i < sz; i++) {
		PyObject* item = PyList_GetItem(*list, i);
		result.push_back(convert(&item));
	}

	return result;
}

PyObject* pyValueFromJsonValue(const gason::JsonValue& value) {
	PyObject* pyValue = nullptr;

	switch (value.getTag()) {
		case gason::JSON_NUMBER:
			pyValue = PyLong_FromSize_t(value.toNumber()); // new ref
			break;
		case gason::JSON_DOUBLE:
			pyValue = PyFloat_FromDouble(value.toDouble()); // new ref
			break;
		case gason::JSON_STRING: {
			auto sv = value.toString();
			pyValue = PyUnicode_FromStringAndSize(sv.data(), sv.size()); // new ref
			break;
		}
		case gason::JSON_NULL:
			pyValue = Py_None;
			Py_INCREF(pyValue); // new ref
			break;
		case gason::JSON_TRUE:
			pyValue = Py_True;
			Py_INCREF(pyValue); // new ref
			break;
		case gason::JSON_FALSE:
			pyValue = Py_False;
			Py_INCREF(pyValue); // new ref
			break;
		case gason::JSON_ARRAY:
			pyValue = PyList_New(0); // new ref
			for (const auto& v : value) {
				PyObject* dictFromJson = pyValueFromJsonValue(v.value); // stolen ref
				PyList_Append(pyValue, dictFromJson); // new ref
				Py_XDECREF(dictFromJson);
			}
			break;
		case gason::JSON_OBJECT:
			pyValue = PyDict_New(); // new ref
			for (const auto& v : value) {
				PyObject* dictFromJson = pyValueFromJsonValue(v.value); // stolen ref
				PyObject* pyKey = PyUnicode_FromStringAndSize(v.key.data(), v.key.size()); // new ref
				PyDict_SetItem(pyValue, pyKey, dictFromJson); // new refs
				Py_XDECREF(pyKey);
				Py_XDECREF(dictFromJson);
			}
			break;
	}

	return pyValue;
}

PyObject* PyObjectFromJson(reindexer::span<char> json) {
	try {
		gason::JsonParser parser;
		auto root = parser.Parse(json);
		return pyValueFromJsonValue(root.value); // stolen ref
	} catch (const gason::Exception& ex) {
		throw reindexer::Error(errParseJson, std::string("PyObjectFromJson: ") + ex.what());
	}
}
}  // namespace pyreindexer

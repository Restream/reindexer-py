#include "pyobjtools.h"

#include <cmath>

namespace pyreindexer {

void pyValueSerialize(PyObject **value, reindexer::WrSerializer &wrSer) {
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
		const char *v = PyUnicode_AsUTF8(*value);
		wrSer.PrintJsonString(v);
	} else if (PyList_Check(*value)) {
		pyListSerialize(value, wrSer);
	} else if (PyDict_Check(*value)) {
		pyDictSerialize(value, wrSer);
	} else {
		throw reindexer::Error(errParseJson, std::string("Unable to parse value of type ") + Py_TYPE(*value)->tp_name);
	}
}

void pyListSerialize(PyObject **list, reindexer::WrSerializer &wrSer) {
	if (!PyList_Check(*list)) {
		throw reindexer::Error(errParseJson, std::string("List expected, got ") + Py_TYPE(*list)->tp_name);
	}

	wrSer << '[';

	unsigned sz = PyList_Size(*list);
	for (unsigned i = 0; i < sz; i++) {
		PyObject *value = PyList_GetItem(*list, i);

		pyValueSerialize(&value, wrSer);

		if (i < sz - 1) {
			wrSer << ',';
		}
	}

	wrSer << ']';
}

void pyDictSerialize(PyObject **dict, reindexer::WrSerializer &wrSer) {
	if (!PyDict_Check(*dict)) {
		throw reindexer::Error(errParseJson, std::string("Dictionary expected, got ") + Py_TYPE(*dict)->tp_name);
	}

	wrSer << '{';

	Py_ssize_t sz = PyDict_Size(*dict);
	if (!sz) {
		wrSer << '}';

		return;
	}

	PyObject *key, *value;
	Py_ssize_t pos = 0;

	while (PyDict_Next(*dict, &pos, &key, &value)) {
		const char *k = PyUnicode_AsUTF8(key);
		wrSer.PrintJsonString(k);
		wrSer << ':';

		pyValueSerialize(&value, wrSer);

		if (pos != sz) {
			wrSer << ',';
		}
	}

	wrSer << '}';
}

void PyObjectToJson(PyObject **obj, reindexer::WrSerializer &wrSer) {
	if (!PyList_Check(*obj) && !PyDict_Check(*obj)) {
		throw reindexer::Error(errParseJson,
							   std::string("PyObject must be a dictionary or a list for JSON serializing, got ") + Py_TYPE(*obj)->tp_name);
	}

	if (PyDict_Check(*obj)) {
		pyDictSerialize(obj, wrSer);
	} else {
		pyListSerialize(obj, wrSer);
	}
}

std::vector<std::string> ParseListToStrVec(PyObject **list) {
	std::vector<std::string> vec;

	Py_ssize_t sz = PyList_Size(*list);
	for (Py_ssize_t i = 0; i < sz; i++) {
		PyObject *item = PyList_GetItem(*list, i);

		if (!PyUnicode_Check(item)) {
			throw reindexer::Error(errParseJson, std::string("String expected, got ") + Py_TYPE(item)->tp_name);
		}

		vec.push_back(PyUnicode_AsUTF8(item));
	}

	return vec;
}

PyObject *pyValueFromJsonValue(const gason::JsonValue &value) {
	PyObject *pyValue = NULL;

	switch (value.getTag()) {
		case gason::JSON_NUMBER:
			pyValue = PyLong_FromSize_t(value.toNumber());
			break;
		case gason::JSON_DOUBLE:
			pyValue = PyFloat_FromDouble(value.toDouble());
			break;
		case gason::JSON_STRING: {
			auto sv = value.toString();
			pyValue = PyUnicode_FromStringAndSize(sv.data(), sv.size());
			break;
		}
		case gason::JSON_NULL:
			pyValue = Py_None;
			break;
		case gason::JSON_TRUE:
			pyValue = Py_True;
			break;
		case gason::JSON_FALSE:
			pyValue = Py_False;
			break;
		case gason::JSON_ARRAY:
			pyValue = PyList_New(0);
			for (const auto &v : value) {
				PyList_Append(pyValue, pyValueFromJsonValue(v.value));
			}
			break;
		case gason::JSON_OBJECT:
			pyValue = PyDict_New();
			for (const auto &v : value) {
				PyDict_SetItem(pyValue, PyUnicode_FromStringAndSize(v.key.data(), v.key.size()), pyValueFromJsonValue(v.value));
			}
			break;
	}

	return pyValue;
}

PyObject *PyObjectFromJson(reindexer::span<char> json) {
	try {
		gason::JsonParser parser;
		auto root = parser.Parse(json);
		// new ref
		return pyValueFromJsonValue(root.value);
	} catch (const gason::Exception &ex) {
		throw reindexer::Error(errParseJson, std::string("PyObjectFromJson: ") + ex.what());
	}
}
}  // namespace pyreindexer

#include "pyobjtools.h"

#include "tools/serializer.h"
#include "vendor/gason/gason.h"

namespace pyreindexer {

void pyValueSerialize(PyObject** value, reindexer::WrSerializer& wrSer);

void pyListSerialize(PyObject** list, reindexer::WrSerializer& wrSer) {
	if (!PyList_Check(*list)) {
		throw reindexer::Error(ErrorCode::errParseJson, std::string("List expected, got ") + Py_TYPE(*list)->tp_name);
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
		throw reindexer::Error(ErrorCode::errParseJson,
								std::string("Dictionary expected, got ") + Py_TYPE(*dict)->tp_name);
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
		throw reindexer::Error(ErrorCode::errParseJson,
								std::string("Unable to parse value of type ") + Py_TYPE(*value)->tp_name);
	}
}

void PyObjectToJson(PyObject** obj, reindexer::WrSerializer& wrSer) {
	if (PyDict_Check(*obj)) {
		pyDictSerialize(obj, wrSer);
	} else if (PyList_Check(*obj)) {
		pyListSerialize(obj, wrSer);
	} else {
		throw reindexer::Error(ErrorCode::errParseJson,
								std::string("PyObject must be a dictionary or a list for JSON serializing, got ")
								+ Py_TYPE(*obj)->tp_name);
	}
}

reindexer::h_vector<std::string, 2> PyObjectToJson(PyObject** obj) {
	reindexer::h_vector<std::string, 2> values;

	reindexer::WrSerializer wrSer;
	if (PyDict_Check(*obj)) {
		Py_ssize_t sz = PyDict_Size(*obj);
		if (sz) {
			PyObject *key = nullptr, *value = nullptr;
			Py_ssize_t pos = 0;
			while (PyDict_Next(*obj, &pos, &key, &value)) {
				const char* k = PyUnicode_AsUTF8(key);
				wrSer.PrintJsonString(k);
				wrSer << ':';
				pyValueSerialize(&value, wrSer);
				values.emplace_back(wrSer.Slice());
				wrSer.Reset();
			}
		}
	} else if (PyList_Check(*obj)) {
		Py_ssize_t sz = PyList_Size(*obj);
		for (Py_ssize_t i = 0; i < sz; ++i) {
			PyObject* value = PyList_GetItem(*obj, i);
			pyValueSerialize(&value, wrSer);
			values.emplace_back(wrSer.Slice());
			wrSer.Reset();
		}
	} else {
		pyValueSerialize(obj, wrSer);
		values.emplace_back(wrSer.Slice());
	}
	return values;
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
	} else if (PyList_Check(*value)) {
		auto size = PyList_Size(*value);
		reindexer::VariantArray array;
		array.reserve(size);
		for (Py_ssize_t i = 0; i < size; ++i) {
			auto item = PyList_GetItem(*value, i);
			array.push_back(convert(&item));
		}
		return reindexer::Variant{array};
	} else if (PyTuple_Check(*value)){
		auto size = PyTuple_Size(*value);
		reindexer::VariantArray array;
		array.reserve(size);
		for (Py_ssize_t i = 0; i < size; ++i) {
			auto item = PyTuple_GetItem(*value, i);
			array.push_back(convert(&item));
		}
		return reindexer::Variant{array};
	} else {
		throw reindexer::Error(ErrorCode::errParseJson,
								std::string("Unexpected type, got ") + Py_TYPE(*value)->tp_name);
	}
	return {};
}

reindexer::VariantArray ParseListToVec(PyObject** list) {
	reindexer::VariantArray result;

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
		case gason::JsonTag::JSON_NUMBER:
			pyValue = PyLong_FromLongLong(value.toNumber()); // new ref
			break;
		case gason::JsonTag::JSON_DOUBLE:
			pyValue = PyFloat_FromDouble(value.toDouble()); // new ref
			break;
		case gason::JsonTag::JSON_STRING: {
			auto sv = value.toString();
			pyValue = PyUnicode_FromStringAndSize(sv.data(), sv.size()); // new ref
			break;
		}
		case gason::JsonTag::JSON_NULL:
			pyValue = Py_None;
			Py_INCREF(pyValue); // new ref
			break;
		case gason::JsonTag::JSON_TRUE:
			pyValue = Py_True;
			Py_INCREF(pyValue); // new ref
			break;
		case gason::JsonTag::JSON_FALSE:
			pyValue = Py_False;
			Py_INCREF(pyValue); // new ref
			break;
		case gason::JsonTag::JSON_ARRAY:
			pyValue = PyList_New(0); // new ref
			for (const auto& v : value) {
				PyObject* dictFromJson = pyValueFromJsonValue(v.value); // stolen ref
				PyList_Append(pyValue, dictFromJson); // new ref
				Py_XDECREF(dictFromJson);
			}
			break;
		case gason::JsonTag::JSON_OBJECT:
			pyValue = PyDict_New(); // new ref
			for (const auto& v : value) {
				PyObject* dictFromJson = pyValueFromJsonValue(v.value); // stolen ref
				PyObject* pyKey = PyUnicode_FromStringAndSize(v.key.data(), v.key.size()); // new ref
				PyDict_SetItem(pyValue, pyKey, dictFromJson); // new refs
				Py_XDECREF(pyKey);
				Py_XDECREF(dictFromJson);
			}
			break;
		case gason::JsonTag::JSON_EMPTY:
			throw gason::Exception("Unexpected `JSON_EMPTY` tag");
			break;
	}

	return pyValue;
}

PyObject* PyObjectFromJson(reindexer::span<char> json) {
	if (json.empty()) {
		PyObject* pyValue = Py_None;
		Py_INCREF(pyValue); // new ref
		return pyValue;
	}

	try {
		gason::JsonParser parser;
		auto root = parser.Parse(json);
		return pyValueFromJsonValue(root.value); // stolen ref
	} catch (const gason::Exception& ex) {
		throw reindexer::Error(ErrorCode::errParseJson, std::string("PyObjectFromJson: ") + ex.what());
	}
}
}  // namespace pyreindexer

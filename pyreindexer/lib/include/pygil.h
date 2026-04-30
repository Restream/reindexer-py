#pragma once

#include <Python.h>

namespace pyreindexer {

// Releases the Python GIL for the lifetime of the object.
// Must be constructed only when the current thread already owns the GIL
// (e.g. inside a Python C-extension call).
class GilRelease {
public:
	GilRelease() noexcept {
#if defined(Py_LIMITED_API)
		// `PyGILState_Check()` is not available in the limited C API.
		// In this build mode we assume correct usage (the caller holds the GIL).
		state_ = PyEval_SaveThread();
#else	// !defined(Py_LIMITED_API)
		// PyEval_SaveThread requires current thread owns the GIL.
		// If used incorrectly, we prefer "no-op" over undefined behavior/crash.
		if (PyGILState_Check()) {
			state_ = PyEval_SaveThread();
		}
#endif	// !defined(Py_LIMITED_API)
	}
	GilRelease(const GilRelease&) = delete;
	GilRelease& operator=(const GilRelease&) = delete;
	GilRelease(GilRelease&&) = delete;
	GilRelease& operator=(GilRelease&&) = delete;
	~GilRelease() noexcept {
		if (state_) {
			PyEval_RestoreThread(state_);
		}
	}

private:
	PyThreadState* state_{nullptr};
};

// Ensures the Python GIL is held for the lifetime of the object.
// Safe to use even when the calling thread does not own the GIL.
class GilAcquire {
public:
	GilAcquire() noexcept : state_{PyGILState_Ensure()} {}
	GilAcquire(const GilAcquire&) = delete;
	GilAcquire& operator=(const GilAcquire&) = delete;
	GilAcquire(GilAcquire&&) = delete;
	GilAcquire& operator=(GilAcquire&&) = delete;
	~GilAcquire() noexcept { PyGILState_Release(state_); }

private:
	PyGILState_STATE state_;
};

}  // namespace pyreindexer

#define PYREINDEXER_DETAIL_CONCAT_INNER(a, b) a##b
#define PYREINDEXER_DETAIL_CONCAT(a, b) PYREINDEXER_DETAIL_CONCAT_INNER(a, b)

// Prefer this macro for large "no Python API" regions.
#define PYREINDEXER_GIL_RELEASE_SCOPE() ::pyreindexer::GilRelease PYREINDEXER_DETAIL_CONCAT(_pyreindexer_gil_release_, __COUNTER__)

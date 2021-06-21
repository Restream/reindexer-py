cmake_minimum_required(VERSION 3.0)

project(pyreindexer)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "RelWithDebInfo")
endif()

enable_testing()

set(PY_MIN_VERSION 3.6)
set(RX_MIN_VERSION 3.2.2)
find_package(PythonInterp ${PY_MIN_VERSION})
find_package(PythonLibs ${PY_MIN_VERSION})
find_package(reindexer CONFIG ${RX_MIN_VERSION})

set(LIB_BUILTIN_NAME "rawpyreindexerb")
set(LIB_CPROTO_NAME "rawpyreindexerc")
set(LIBS_EXT ".so")

set(LIBSRC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/lib/src)
set(RESOURCES_DIR ${CMAKE_CURRENT_SOURCE_DIR}/lib/include)

file(GLOB_RECURSE SRCS ${RESOURCES_DIR}/*.cc ${LIBSRC_DIR}/*.cc)

include_directories(
    ${LIBSRC_DIR}
    ${RESOURCES_DIR}
    ${PYTHON_INCLUDE_DIRS}
    ${REINDEXER_INCLUDE_DIRS})

link_directories(
    ${REINDEXER_LIB_DIR}
    ${REINDEXER_LINK_DIRS})

add_library(${LIB_BUILTIN_NAME} SHARED ${SRCS})
add_library(${LIB_CPROTO_NAME} SHARED ${SRCS})

target_link_libraries(${LIB_BUILTIN_NAME} ${PYTHON_LIBRARIES} ${REINDEXER_LIBRARIES})
target_link_libraries(${LIB_CPROTO_NAME} ${PYTHON_LIBRARIES} ${REINDEXER_LIBRARIES})
target_compile_definitions(${LIB_CPROTO_NAME} PRIVATE PYREINDEXER_CPROTO=1)

set_target_properties(${LIB_BUILTIN_NAME} PROPERTIES SUFFIX ${LIBS_EXT})
set_target_properties(${LIB_CPROTO_NAME} PROPERTIES SUFFIX ${LIBS_EXT})

# python does not allow 'lib' prefix
set_target_properties(${LIB_BUILTIN_NAME} PROPERTIES PREFIX "")
set_target_properties(${LIB_CPROTO_NAME} PROPERTIES PREFIX "")

if (WITH_GCOV)
    target_link_libraries(${LIB_BUILTIN_NAME} -fprofile-arcs)
    target_link_libraries(${LIB_CPROTO_NAME} -fprofile-arcs)
endif (WITH_GCOV)

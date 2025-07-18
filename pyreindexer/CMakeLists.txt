cmake_minimum_required(VERSION 3.18)

project(pyreindexer)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "RelWithDebInfo")
endif()

enable_testing()

option(CIBUILDWHEEL "Is cibuildwheel environment" OFF)
if(DEFINED ENV{CIBUILDWHEEL} AND "$ENV{CIBUILDWHEEL}" STREQUAL "1")
    set(CIBUILDWHEEL ON)
endif()

set(PY_MIN_VERSION 3.8)
set(RX_MIN_VERSION 5.4.0)
if(CIBUILDWHEEL)
    file(GLOB PYTHON_INCLUDE_DIRS "/opt/python/*/include/python*")
    include_directories(SYSTEM ${PYTHON_INCLUDE_DIRS})
else()
    find_package(PythonInterp ${PY_MIN_VERSION} REQUIRED)
    find_package(PythonLibs ${PY_MIN_VERSION} REQUIRED)
endif()
find_package(reindexer CONFIG ${RX_MIN_VERSION} REQUIRED)

option(WITH_GCOV "Enable instrumented code coverage build" OFF)

set(LIB_BUILTIN_NAME "rawpyreindexerb")
set(LIB_CPROTO_NAME "rawpyreindexerc")
set(LIBS_EXT ".so")

set(LIBSRC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/lib/src)
set(RESOURCES_DIR ${CMAKE_CURRENT_SOURCE_DIR}/lib/include)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -Werror -Wswitch-enum")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++20 -Wall -Wextra -Werror -Wswitch-enum -Wno-unused-parameter -fexceptions")
string(REPLACE "-O2" "-O3" CMAKE_CXX_FLAGS_RELWITHDEBINFO "${CMAKE_CXX_FLAGS_RELWITHDEBINFO}")

if(CIBUILDWHEEL)
    set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -s")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -s")
endif()

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
    target_link_libraries(${LIB_BUILTIN_NAME} -fprofile-arcs -ftest-coverage)
    target_link_libraries(${LIB_CPROTO_NAME} -fprofile-arcs -ftest-coverage)
endif (WITH_GCOV)

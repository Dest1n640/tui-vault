cmake_minimum_required(VERSION 3.15)

project(CoreModule)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(Python REQUIRED COMPONENTS Interpreter Development)

include(FetchContent)

FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
)

FetchContent_Declare(
  sodium
  GIT_REPOSITORY https://github.com/robinlinden/libsodium-cmake.git
)

FetchContent_Declare(
  spdlog
  GIT_REPOSITORY https://github.com/gabime/spdlog.git
  GIT_TAG v1.x
)

FetchContent_MakeAvailable(sodium pybind11 spdlog)

pybind11_add_module(core_module src/crypto.cpp)

target_link_libraries(core_module PRIVATE sodium spdlog)

set_target_properties(core_module PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${PROJECT_SOURCE_DIR}/../tui_vault"
)

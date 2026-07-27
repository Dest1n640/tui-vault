cmake_minimum_required(VERSION 3.15)

project(CoreModule)

find_package(Python REQUIRED COMPONENTS Interpreter Development)

find_package(pybind11 REQUIRED)

pybind11_add_module(core_module src/crypto.cpp)

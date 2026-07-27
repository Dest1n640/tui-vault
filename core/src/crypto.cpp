#include <pybind11/pybind11.h>
#include <string>

namespace py = pybind11;

std::string ModifyString(std::string input) { return "Hello World " + input; }

PYBIND11_MODULE(code_module, m, py::mod_gil_not_used()) {
  m.doc() = "Hello";
  m.def("ModifyString", &ModifyString, "A function that modify string");
}

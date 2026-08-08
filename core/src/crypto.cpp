#include <pybind11/pybind11.h>
#include <sodium.h>
#include <string>
#include <vector>
#include <spdlog/spdlog.h>

namespace py = pybind11;

std::vector<uint8_t> crypto_key(std::vector<uint8_t> key){
  std::vector<uint8_t> vec;
  auto sodium = sodium_init();
  if (sodium < 0){
    spdlog::error("Sodium initialization error");
    return vec;
  }
  
  auto crypto_key = crypto_pwhash(key);
  return crypto_key;
}

PYBIND11_MODULE(core_module, m, py::mod_gil_not_used()) {
  m.doc() = "Crypto key";
  m.def("crypto_key", &crypto_key, "A function that hash key");
}

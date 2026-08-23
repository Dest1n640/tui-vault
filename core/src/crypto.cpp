#include <pybind11/pybind11.h>
#include <sodium.h>
#include <string>
#include <vector>
#include <spdlog/spdlog.h>
#include <pybind11/stl.h>

namespace py = pybind11;

std::vector<uint8_t> crypto_key(const std::string& password, const std::vector<uint8_t>& salt){

  std::vector<uint8_t> key(crypto_secretbox_KEYBYTES);

  if (salt.size() != crypto_pwhash_SALTBYTES){
    spdlog::error("Invalid salt size");
    throw std::invalid_argument("Invalid salt size"); 
  }

  auto crypto_key = crypto_pwhash(
      key.data(),
      key.size(),
      password.c_str(),
      password.size(),
      salt.data(),
      crypto_pwhash_OPSLIMIT_INTERACTIVE,
      crypto_pwhash_MEMLIMIT_INTERACTIVE,
      crypto_pwhash_ALG_DEFAULT
  );

  if (crypto_key != 0){
    spdlog::error("Not enough memory");
    throw std::runtime_error("Key derivation failed");
  }

  spdlog::info("Master key generated");
  return key;
}

PYBIND11_MODULE(core_module, m, py::mod_gil_not_used()) {
  auto sodium = sodium_init();

  if (sodium < 0){
    spdlog::error("Sodium initialization error");
    throw std::runtime_error("Failed to initialize libsodium");
  }


  m.doc() = "Crypto key";
  m.def("crypto_key", &crypto_key, "A function that hash key");
}

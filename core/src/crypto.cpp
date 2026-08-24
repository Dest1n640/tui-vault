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

  spdlog::debug("Master key generated");
  return key;
}

std::pair<std::vector<uint8_t>, std::vector<uint8_t>> encrypt_data(const std::string& plaintext, const std::vector<uint8_t>& key){
  std::vector<uint8_t> nonce(crypto_aead_xchacha20poly1305_ietf_NPUBBYTES);
  std::vector<uint8_t> ciphertext(plaintext.size() + crypto_aead_xchacha20poly1305_ietf_ABYTES);
  randombytes_buf(nonce.data(), nonce.size());

  int res = crypto_aead_xchacha20poly1305_ietf_encrypt(
      ciphertext.data(),
      NULL,
      reinterpret_cast<const unsigned char*>(plaintext.data()),
      plaintext.size(),
      NULL,
      0,
      NULL,
      nonce.data(),
      key.data()
  );

  if (res != 0) {
      spdlog::error("Encryption failed");
      throw std::runtime_error("Encryption failed");
  }
  spdlog::debug("Encryption success");
  return {nonce, ciphertext};
}

std::string decrypt_data(const std::vector<uint8_t>& ciphertext, const std::vector<uint8_t> key, const std::vector<uint8_t> nonce){
  if (ciphertext.size() < crypto_aead_xchacha20poly1305_ietf_ABYTES) {
    spdlog::error("Ciphertext too short");
    throw std::invalid_argument("Ciphertext too short");
  }

  size_t decrypted_len = ciphertext.size() - crypto_aead_xchacha20poly1305_ietf_ABYTES;
  std::vector<uint8_t> decrypted(decrypted_len, '\0');

  int res = crypto_aead_xchacha20poly1305_ietf_decrypt(
    reinterpret_cast<unsigned char*>(decrypted.data()),
    NULL,
    NULL,
    ciphertext.data(),
    ciphertext.size(),
    NULL,
    0, 
    nonce.data(),
    key.data()
  );

  if (res != 0){
    spdlog::error("Decryption failed");
    throw std::runtime_error("Decryption failed");
  }

  spdlog::debug("Decription success");
  return std::string(decrypted.begin(), decrypted.end());
}

PYBIND11_MODULE(core_module, m, py::mod_gil_not_used()) {
  auto sodium = sodium_init();

  if (sodium < 0){
    spdlog::error("Sodium initialization error");
    throw std::runtime_error("Failed to initialize libsodium");
  }


  m.doc() = "Crypto key";
  m.def("crypto_key", &crypto_key, "A function that hash key");
  m.def("encrypt_data", &encrypt_data, "A function for encrypt key");
  m.def("decrypt_data", &decrypt_data, "A function for decrypt key");
}

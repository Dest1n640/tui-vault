import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "core" / "build"))

from core_module import crypto_key, encrypt_data, decrypt_data


def test_crypto_key(password, salt):
  try:
      key = crypto_key(password, list(salt))
      return key
  except ValueError as e:
      print("Caught expected error:", e)

def test_encrypt_data(text, key):
   nonce, ciphertext = encrypt_data(text, key)
   return nonce, ciphertext

def test_decrypt_data(ciphertext, key, nonce):
   text = decrypt_data(ciphertext, key, nonce)
   return text

def test_encrypt_decrypt_data_eq(text, key):
   nonce, ciphertext = encrypt_data(text, key)
   text_out = decrypt_data(ciphertext, key, nonce)
   if text != text_out:
      raise ValueError
  

key = test_crypto_key("My_password", os.urandom(16)) # Тест1
test_crypto_key("My_password", os.urandom(10))
print("=" * 50)
nonce, ciphertext = test_encrypt_data("Text", key) # Тест2
print("=" * 50)
test_decrypt_data(ciphertext, key, nonce) # Тест3
print("=" * 50) 
test_encrypt_decrypt_data_eq("Text", key) #Тест4


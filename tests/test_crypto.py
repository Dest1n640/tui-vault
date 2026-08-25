import sys
import os
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "core" / "build"))

from core_module import crypto_key, encrypt_data, decrypt_data

@pytest.fixture
def master_key():
    password = "Master_password"
    salt = list(os.urandom(16))
    return crypto_key(password, salt)

@pytest.mark.parametrize("invalid_salt_len", [0, 10, 15, 17, 32])
def test_crypto_key_invalid_salt(invalid_salt_len):
    password = "Master_password"
    salt = list(os.urandom(invalid_salt_len))
    with pytest.raises(ValueError):
        crypto_key(password, salt)


@pytest.mark.parametrize("payload", [
    "",
    "Simple secret",
    '{"service": "github", "login": "user", "password": "123"}',
    "Тест с русскими буквами"
])
def test_encryption_roundtrip(master_key, payload):
    nonce, ciphertext = encrypt_data(payload, master_key)
    decrypted = decrypt_data(ciphertext, master_key, nonce)
    assert decrypted == payload

# TODO: дописать тесты для проверки целостности данных, аутентификации, передача шифротекста <16 байт

import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "core" / "build"))

from core_module import crypto_key

password = "My_secret_password"
salt_true = os.urandom(16)
salt_false = os.urandom(10)

print(crypto_key(password, list(salt_true)))

try:
    crypto_key(password, list(salt_false))
except ValueError as e:
    print("Caught expected error:", e)

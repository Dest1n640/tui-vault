import json
import os
from pathlib import Path
from uuid import UUID, uuid4

from core_module import crypto_key, decrypt_data, encrypt_data
from pydantic import BaseModel, Field


class VaultItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    service: str
    login: str | None = None
    password: str | None = None
    notes: str | None = None


class VaultManager:
    SALT_LEN = 16
    NONCE_LEN = 24

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self._key: list[int] | None = None
        self._salt: bytes | None = None

    def create_vault(self, master_password: str) -> None:
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self._salt = os.urandom(self.SALT_LEN)
        key = crypto_key(master_password, list(self._salt))
        nonce, ciphertext = encrypt_data("[]", key)
        self.filepath.write_bytes(self._salt + bytes(nonce) + bytes(ciphertext))

    def unlock_vault(self, master_password: str) -> list[VaultItem]:
        data = self.filepath.read_bytes()
        if len(data) < self.SALT_LEN + self.NONCE_LEN + 16:
            raise ValueError("Data size less the need")

        self._salt = data[: self.SALT_LEN]
        nonce = data[self.SALT_LEN : self.SALT_LEN + self.NONCE_LEN]
        ciphertext = data[self.SALT_LEN + self.NONCE_LEN :]
        self._key = crypto_key(master_password, list(self._salt))
        raw_json = decrypt_data(list(ciphertext), self._key, list(nonce))
        vault = [VaultItem.model_validate(item) for item in json.loads(raw_json)]
        return vault

    def save_vault(self, items: list[VaultItem]):
        if self._key is None or self._salt is None:
            raise RuntimeError("Vault is not unlocked or initialized")

        raw_json = json.dumps([item.model_dump(mode="json") for item in items])
        nonce, ciphertext = encrypt_data(raw_json, self._key)
        self.filepath.write_bytes(self._salt + bytes(nonce) + bytes(ciphertext))

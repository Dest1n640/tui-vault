from enum import Enum
from pathlib import Path
from uuid import UUID

from storage import VaultManager, VaultItem

MAIN_DIRECTORY = Path.home() / ".config" / "tui_vault" / "vault.bin"

class State(Enum):
  LOCKED = 'Locked'
  UNLOCKED = 'Unlocked'
  FIRST_RUN = 'First_run'

class Session:
  def __init__(self):
    self.vault_manager = VaultManager(MAIN_DIRECTORY)
    self.state = State.LOCKED if MAIN_DIRECTORY.exists() else State.FIRST_RUN
    self.items = []

  def create_session(self, master_password: str):
    if self.state == State.FIRST_RUN:
      self.vault_manager.create_vault(master_password)
      self.state = State.UNLOCKED
    

  def unlock(self, master_password: str):
    if self.state == State.LOCKED:
      self.items = self.vault_manager.unlock_vault(master_password)
      self.state = State.UNLOCKED
    return self.items

  def lock(self):
    if self.state == State.UNLOCKED:
      self.vault_manager.save_vault(self.items)
      self.items = []
      self.state = State.LOCKED

  def add_item(self, item: VaultItem):
    if self.state == State.LOCKED:
      raise ValueError("Session is locked")
    self.items.append(item)
    self.vault_manager.save_vault(self.items)
    return self.items

  def get_items(self):
    return self.items

  def delete_items(self, id: UUID):
    self.items = [item for item in self.items if item.id != id]
    self.vault_manager.save_vault(self.items)
    return self.items

  def update_items(self, update_item: VaultItem):
    for ind, item in enumerate(self.items):
      if item.id == update_item.id:
        self.items[ind] = update_item
        self.vault_manager.save_vault(self.items)
        return self.items

    raise KeyError(f"Item with id={update_item.id} not found")

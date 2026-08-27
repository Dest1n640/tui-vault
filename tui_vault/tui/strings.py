"""Все пользовательские строки интерфейса — в одном месте.

Экраны никогда не содержат текстовых литералов: они обращаются к словарю
``S``. Чтобы добавить язык, достаточно объявить рядом второй словарь с теми
же ключами и переключать ``S`` — переписывать вёрстку экранов не придётся.
"""

EN: dict[str, str] = {
    "app.title": "tui-vault",
    # --- Экран аутентификации -------------------------------------------
    "auth.create.title": "Create master password",
    "auth.create.subtitle": (
        "This password encrypts your vault. There is no way to recover it."
    ),
    "auth.create.password": "Master password",
    "auth.create.confirm": "Confirm master password",
    "auth.unlock.title": "Unlock vault",
    "auth.unlock.subtitle": "Enter your master password to decrypt the vault.",
    "auth.unlock.password": "Master password",
    "auth.error.too_short": "Master password must be at least {minimum} characters.",
    "auth.error.mismatch": "Passwords do not match.",
    "auth.error.wrong_password": "Wrong master password.",
    "auth.error.unexpected": "Could not open the vault: {error}",
    # --- Экран со списком записей ---------------------------------------
    "vault.empty": 'No entries yet. Press "a" to add one.',
    "vault.no_password": "This entry has no password to copy.",
    "vault.deleted": 'Deleted "{service}".',
    "vault.added": 'Added "{service}".',
    "vault.updated": 'Updated "{service}".',
    "vault.locked": "Vault locked.",
    # --- Форма записи ----------------------------------------------------
    "form.new.title": "New entry",
    "form.edit.title": "Edit entry",
    "form.service": "Service",
    "form.login": "Login",
    "form.password": "Password",
    "form.notes": "Notes",
    "form.service.placeholder": "github.com",
    "form.login.placeholder": "optional",
    "form.password.placeholder": "optional",
    "form.error.service_required": "Service is required.",
    "form.hint": "ctrl+s save · esc cancel · ctrl+r reveal · ctrl+y copy",
    # --- Диалог удаления --------------------------------------------------
    "confirm.title": "Delete entry",
    "confirm.message": 'Delete entry "{service}" ({id})? This cannot be undone.',
    "confirm.cancel": "Cancel",
    "confirm.delete": "Delete",
    # --- Буфер обмена -----------------------------------------------------
    "clipboard.copied": "Password copied. Clipboard clears in {seconds}s.",
    "clipboard.unavailable": "Clipboard unavailable: {error}",
    # --- Подписи клавиш в Footer -----------------------------------------
    "keys.quit": "Quit",
    "keys.add": "Add",
    "keys.edit": "Edit",
    "keys.delete": "Delete",
    "keys.copy": "Copy password",
    "keys.lock": "Lock",
    "keys.save": "Save",
    "keys.cancel": "Cancel",
    "keys.reveal": "Show/hide",
}

S = EN

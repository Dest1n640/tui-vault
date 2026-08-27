"""Работа с системным буфером обмена.

Обёртка над pyperclip: приложение не должно падать из-за того, что в
системе нет ``pbcopy``/``xclip``. Таймер автоочистки живёт на уровне
приложения (см. ``TuiVault.copy_secret``), здесь только сами операции.
"""

import pyperclip

CLEAR_AFTER_SECONDS = 20.0
"""Через сколько секунд стереть скопированный пароль из буфера."""


class ClipboardUnavailable(RuntimeError):
    """В системе нет доступного механизма буфера обмена."""


def copy(text: str) -> None:
    try:
        pyperclip.copy(text)
    except pyperclip.PyperclipException as exc:
        raise ClipboardUnavailable(str(exc)) from exc


def clear_if_holds(text: str) -> None:
    """Очистить буфер, только если там всё ещё лежит наш секрет.

    Проверка нужна, чтобы не затереть то, что пользователь скопировал
    уже после нас — иначе автоочистка воровала бы чужие данные.
    """
    try:
        if pyperclip.paste() == text:
            pyperclip.copy("")
    except pyperclip.PyperclipException:
        pass

"""Точка сборки интерфейса: приложение, роутинг экранов, буфер обмена."""

from textual.app import App
from textual.binding import Binding
from textual.timer import Timer

from ..session import Session
from . import clipboard
from .screens.auth import AuthScreen
from .screens.vault import VaultScreen
from .strings import S


class TuiVault(App[None]):
    CSS_PATH = "app.tcss"
    TITLE = S["app.title"]

    BINDINGS = [
        Binding("ctrl+q", "quit", S["keys.quit"], priority=True),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.session = Session()
        self._clear_timer: Timer | None = None
        self._copied: str | None = None

    def on_mount(self) -> None:
        self.push_screen(AuthScreen())


    def show_vault(self) -> None:
        self.switch_screen(VaultScreen())

    def lock(self) -> None:
        """Заблокировать хранилище и вернуться на экран ввода пароля."""
        self.forget_copied_secret()
        self.session.lock()
        self.switch_screen(AuthScreen())
        self.notify(S["vault.locked"])


    def copy_secret(self, secret: str) -> None:
        """Скопировать пароль и завести таймер автоочистки."""
        try:
            clipboard.copy(secret)
        except clipboard.ClipboardUnavailable as exc:
            self.notify(
                S["clipboard.unavailable"].format(error=exc),
                severity="error",
            )
            return

        self._copied = secret
        if self._clear_timer is not None:
            self._clear_timer.stop()
        self._clear_timer = self.set_timer(
            clipboard.CLEAR_AFTER_SECONDS,
            self.forget_copied_secret,
        )
        self.notify(
            S["clipboard.copied"].format(seconds=int(clipboard.CLEAR_AFTER_SECONDS))
        )

    def forget_copied_secret(self) -> None:
        """Стереть наш пароль из буфера, если он всё ещё там.

        Намеренно НЕ вызывается при выходе из приложения: главный сценарий
        продукта — скопировать пароль, выйти и вставить его в браузере.
        Очистка на выходе ломала бы его. Таймер работает, пока приложение
        живо, плюс явная блокировка по ctrl+l.
        """
        if self._clear_timer is not None:
            self._clear_timer.stop()
            self._clear_timer = None
        if self._copied is not None:
            clipboard.clear_if_holds(self._copied)
            self._copied = None

"""Экран аутентификации: создание мастер-пароля либо разблокировка."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Input, Static

from ...errors import WrongPasswordError
from ...session import State
from ..strings import S

MIN_PASSWORD_LENGTH = 8


class AuthScreen(Screen[None]):
    """Один экран в двух режимах — их выбирает состояние сессии.

    FIRST_RUN: два поля, пароль + подтверждение, создаём хранилище.
    LOCKED: одно поле, расшифровываем существующее хранилище.
    """

    def __init__(self) -> None:
        super().__init__()
        self._first_run = False

    def compose(self) -> ComposeResult:
        self._first_run = self.app.session.state is State.FIRST_RUN

        title = "auth.create.title" if self._first_run else "auth.unlock.title"
        subtitle = "auth.create.subtitle" if self._first_run else "auth.unlock.subtitle"
        placeholder = (
            "auth.create.password" if self._first_run else "auth.unlock.password"
        )

        yield Header()
        with Vertical(id="auth-box"):
            yield Static(S[title], id="auth-title")
            yield Static(S[subtitle], classes="muted")
            yield Input(placeholder=S[placeholder], password=True, id="password")
            if self._first_run:
                yield Input(
                    placeholder=S["auth.create.confirm"],
                    password=True,
                    id="confirm",
                )
            yield Static("", id="auth-error", classes="error")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#password", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if self._first_run and event.input.id == "password":
            self.query_one("#confirm", Input).focus()
            return
        self._submit()

    def _submit(self) -> None:
        password = self.query_one("#password", Input).value
        if self._first_run:
            self._create(password)
        else:
            self._unlock(password)

    def _create(self, password: str) -> None:
        confirm = self.query_one("#confirm", Input).value

        if len(password) < MIN_PASSWORD_LENGTH:
            self._fail(S["auth.error.too_short"].format(minimum=MIN_PASSWORD_LENGTH))
            return
        if password != confirm:
            self._fail(S["auth.error.mismatch"])
            return

        try:
            self.app.session.create_session(password)
        except Exception as exc:  # хранилище не должно ронять интерфейс
            self._fail(S["auth.error.unexpected"].format(error=exc))
            return

        self.app.show_vault()

    def _unlock(self, password: str) -> None:
        try:
            self.app.session.unlock(password)
        except WrongPasswordError:
            self._fail(S["auth.error.wrong_password"])
        except Exception as exc:  # битый файл, нехватка памяти и прочее
            self._fail(S["auth.error.unexpected"].format(error=exc))
        else:
            self.app.show_vault()

    def _fail(self, message: str) -> None:
        self.query_one("#auth-error", Static).update(message)
        for field in self.query(Input):
            field.value = ""
        self.query_one("#password", Input).focus()

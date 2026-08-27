"""Модальная форма создания и редактирования записи."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Label, Static, TextArea

from ...storage import VaultItem
from ..strings import S


class EntryFormScreen(ModalScreen[VaultItem | None]):
    """Одна форма на оба сценария: ``item=None`` — создание, иначе правка.

    Возвращает собранный ``VaultItem`` (у правки — с прежним id) либо
    ``None``, если пользователь отменил ввод. Сохранением в хранилище
    занимается вызывающий экран, форма только собирает данные.
    """

    BINDINGS = [
        Binding("ctrl+s", "save", S["keys.save"]),
        Binding("escape", "cancel", S["keys.cancel"]),
        Binding("ctrl+r", "toggle_password", S["keys.reveal"]),
        # priority: в поле Notes TextArea вешает на ctrl+y свой redo.
        Binding("ctrl+y", "copy_password", S["keys.copy"], priority=True),
    ]

    def __init__(self, item: VaultItem | None = None) -> None:
        super().__init__()
        self.item = item

    def compose(self) -> ComposeResult:
        editing = self.item is not None

        with Vertical(id="form-box"):
            yield Static(
                S["form.edit.title"] if editing else S["form.new.title"],
                id="form-title",
            )

            yield Label(S["form.service"])
            yield Input(
                value=self.item.service if editing else "",
                placeholder=S["form.service.placeholder"],
                id="service",
            )

            yield Label(S["form.login"])
            yield Input(
                value=(self.item.login or "") if editing else "",
                placeholder=S["form.login.placeholder"],
                id="login",
            )

            yield Label(S["form.password"])
            yield Input(
                value=(self.item.password or "") if editing else "",
                placeholder=S["form.password.placeholder"],
                password=True,
                id="password",
            )

            yield Label(S["form.notes"])
            yield TextArea(
                (self.item.notes or "") if editing else "",
                id="notes",
            )

            yield Static("", id="form-error", classes="error")
            yield Static(S["form.hint"], classes="muted")

    def on_mount(self) -> None:
        self.query_one("#service", Input).focus()

    def action_save(self) -> None:
        service = self.query_one("#service", Input).value.strip()
        if not service:
            self.query_one("#form-error", Static).update(
                S["form.error.service_required"]
            )
            self.query_one("#service", Input).focus()
            return

        fields = {
            "service": service,
            "login": _or_none(self.query_one("#login", Input).value),
            "password": _or_none(self.query_one("#password", Input).value),
            "notes": _or_none(self.query_one("#notes", TextArea).text),
        }
        if self.item is not None:
            fields["id"] = self.item.id

        self.dismiss(VaultItem(**fields))

    def action_cancel(self) -> None:
        self.dismiss(None)

    def action_toggle_password(self) -> None:
        field = self.query_one("#password", Input)
        field.password = not field.password

    def action_copy_password(self) -> None:
        password = self.query_one("#password", Input).value
        if not password:
            self.notify(S["vault.no_password"], severity="warning")
            return
        self.app.copy_secret(password)


def _or_none(value: str) -> str | None:
    """Пустое поле — это отсутствие значения, а не пустая строка."""
    return value.strip() or None

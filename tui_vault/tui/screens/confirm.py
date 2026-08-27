"""Модальное подтверждение удаления записи."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static

from ...storage import VaultItem
from ..strings import S
from ..widgets.entry_card import SHORT_ID_LENGTH


class ConfirmDeleteScreen(ModalScreen[bool]):
    """Возвращает True, если пользователь подтвердил удаление."""

    BINDINGS = [
        Binding("y", "confirm", S["confirm.delete"]),
        Binding("n", "cancel", S["confirm.cancel"]),
        Binding("escape", "cancel", "", show=False),
        Binding("left", "app.focus_previous", "", show=False),
        Binding("right", "app.focus_next", "", show=False),
    ]

    def __init__(self, item: VaultItem) -> None:
        super().__init__()
        self.item = item

    def compose(self) -> ComposeResult:
        message = S["confirm.message"].format(
            service=self.item.service,
            id=str(self.item.id)[:SHORT_ID_LENGTH],
        )
        with Vertical(id="confirm-box"):
            yield Static(S["confirm.title"], id="confirm-title")
            # markup=False: название сервиса вводит пользователь.
            yield Static(message, markup=False, id="confirm-message")
            with Horizontal(id="confirm-buttons"):
                yield Button(S["confirm.cancel"], id="cancel")
                yield Button(S["confirm.delete"], variant="error", id="delete")

    def on_mount(self) -> None:
        self.query_one("#cancel", Button).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "delete")

    def action_confirm(self) -> None:
        self.dismiss(True)

    def action_cancel(self) -> None:
        self.dismiss(False)

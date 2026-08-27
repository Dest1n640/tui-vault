"""«Квадратик» одной записи в списке хранилища."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from ...storage import VaultItem

SHORT_ID_LENGTH = 8


class EntryCard(Vertical):
    """Карточка записи: сервис крупно, логин и короткий id — подписью.

    Карточка фокусируемая: выделенная запись — это просто запись с
    фокусом, поэтому прокрутку к ней и подсветку берёт на себя Textual.
    """

    can_focus = True

    def __init__(self, item: VaultItem) -> None:
        super().__init__()
        self.item = item

    def compose(self) -> ComposeResult:
        yield Static(self.item.service, markup=False, classes="card-service")
        yield Static(self._meta(), markup=False, classes="card-meta")

    def _meta(self) -> str:
        short_id = str(self.item.id)[:SHORT_ID_LENGTH]
        if self.item.login:
            return f"{self.item.login} · {short_id}"
        return short_id

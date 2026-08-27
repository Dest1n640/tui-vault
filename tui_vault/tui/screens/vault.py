"""Главный экран: список записей и все действия над ними."""

from uuid import UUID

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from ...storage import VaultItem
from ..strings import S
from ..widgets.entry_card import EntryCard
from .confirm import ConfirmDeleteScreen
from .entry_form import EntryFormScreen


class VaultScreen(Screen[None]):
    BINDINGS = [
        Binding("up", "cursor_up", "", show=False),
        Binding("down", "cursor_down", "", show=False),
        Binding("c", "copy_password", S["keys.copy"]),
        Binding("enter", "edit", S["keys.edit"]),
        Binding("a", "add", S["keys.add"]),
        Binding("d", "delete", S["keys.delete"]),
        Binding("ctrl+l", "lock", S["keys.lock"]),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(id="entries")
        yield Footer()

    async def on_mount(self) -> None:
        await self.refresh_entries()

    async def refresh_entries(self, select: UUID | None = None) -> None:
        """Перерисовать список, по возможности сохранив выделение."""
        container = self.query_one("#entries", VerticalScroll)
        previous = self._cards()
        fallback = previous.index(self.focused) if self.focused in previous else 0

        await container.remove_children()

        items = sorted(
            self.app.session.get_items(),
            key=lambda item: item.service.lower(),
        )
        if not items:
            await container.mount(Static(S["vault.empty"], id="vault-empty"))
            return

        cards = [EntryCard(item) for item in items]
        await container.mount_all(cards)

        index = fallback
        if select is not None:
            index = next(
                (i for i, card in enumerate(cards) if card.item.id == select),
                fallback,
            )
        cards[min(index, len(cards) - 1)].focus()

    def action_cursor_up(self) -> None:
        self._move(-1)

    def action_cursor_down(self) -> None:
        self._move(1)

    def _cards(self) -> list[EntryCard]:
        # query отдаёт виджеты в порядке DOM, то есть в порядке сортировки.
        return list(self.query(EntryCard))

    def _move(self, delta: int) -> None:
        cards = self._cards()
        if not cards:
            return
        current = cards.index(self.focused) if self.focused in cards else 0
        cards[max(0, min(current + delta, len(cards) - 1))].focus()

    def _current_item(self) -> VaultItem | None:
        focused = self.focused
        return focused.item if isinstance(focused, EntryCard) else None

    def action_copy_password(self) -> None:
        item = self._current_item()
        if item is None:
            return
        if not item.password:
            self.notify(S["vault.no_password"], severity="warning")
            return
        self.app.copy_secret(item.password)

    def action_lock(self) -> None:
        self.app.lock()

    @work
    async def action_add(self) -> None:
        result = await self.app.push_screen_wait(EntryFormScreen())
        if result is None:
            return
        self.app.session.add_item(result)
        await self.refresh_entries(select=result.id)
        self.notify(S["vault.added"].format(service=result.service))

    @work
    async def action_edit(self) -> None:
        item = self._current_item()
        if item is None:
            return
        result = await self.app.push_screen_wait(EntryFormScreen(item))
        if result is None:
            return
        self.app.session.update_items(result)
        await self.refresh_entries(select=result.id)
        self.notify(S["vault.updated"].format(service=result.service))

    @work
    async def action_delete(self) -> None:
        item = self._current_item()
        if item is None:
            return
        if not await self.app.push_screen_wait(ConfirmDeleteScreen(item)):
            return
        self.app.session.delete_items(item.id)
        await self.refresh_entries()
        self.notify(S["vault.deleted"].format(service=item.service))

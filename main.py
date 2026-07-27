from textual.app import App, ComposeResult
from textual.widgets import Footer, Header


class TuiVault(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()


if __name__ == "__main__":
    app = TuiVault()
    app.run()

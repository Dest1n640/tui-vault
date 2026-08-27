"""Точка входа: uv run python -m tui_vault"""

from .tui.app import TuiVault


def main() -> None:
    TuiVault().run()


if __name__ == "__main__":
    main()

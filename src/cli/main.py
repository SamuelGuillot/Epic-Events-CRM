import src.models  # noqa: F401

from src.cli.app import app
from src.cli.commands import auth_commands       # noqa: F401
from src.cli.commands import client_commands     # noqa: F401
from src.cli.commands import contract_commands   # noqa: F401
from src.cli.commands import event_commands      # noqa: F401


def main():
    app()


if __name__ == "__main__":
    main()
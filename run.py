import src.models  # noqa: F401

from src.cli import auth_commands
from src.cli import client_commands
from src.cli import contract_commands
from src.cli import event_commands
from src.cli.app import app

if __name__ == "__main__":
    app()
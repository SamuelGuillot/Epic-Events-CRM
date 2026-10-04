import src.models

from src.cli.app import app
from src.cli.commands import auth_commands
from src.cli.commands import client_commands
from src.cli.commands import contract_commands
from src.cli.commands import event_commands
from src.cli.commands import menu_commands


if __name__ == "__main__":
    app()
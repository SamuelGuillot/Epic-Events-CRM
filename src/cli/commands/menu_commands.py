import inspect
import typer
import questionary
from rich.console import Console
from src.cli.app import app


console = Console()


@app.command()
def menu():
    """Menu interactif pour naviguer dans le CRM."""
    console.print("[bold cyan]====== Epic Events CRM ======[/bold cyan]")

    while True:
        choice = questionary.select(
            "Que voulez-vous faire ?",
            choices=[
                "Clients",
                "Contrats",
                "Evenements",
                "Authentification",
                "Quitter",
            ],
        ).ask()

        if choice is None or choice == "Quitter":
            console.print("[yellow]A bientot ![/yellow]")
            return

        if choice == "Clients":
            _menu_clients()
        elif choice == "Contrats":
            _menu_contracts()
        elif choice == "Evenements":
            _menu_events()
        elif choice == "Authentification":
            _menu_auth()


def _menu_clients():
    action = questionary.select(
        "Action sur les clients ?",
        choices=["Lister", "Creer", "Modifier", "Retour"],
    ).ask()

    if action is None or action == "Retour":
        return

    if action == "Lister":
        _call_command("client-list")
    elif action == "Creer":
        _call_command("client-create")
    elif action == "Modifier":
        _call_command("client-update")


def _menu_contracts():
    action = questionary.select(
        "Action sur les contrats ?",
        choices=["Lister", "Creer", "Modifier", "Retour"],
    ).ask()

    if action is None or action == "Retour":
        return

    if action == "Lister":
        _call_command("contract-list")
    elif action == "Creer":
        _call_command("contract-create")
    elif action == "Modifier":
        _call_command("contract-update")


def _menu_events():
    action = questionary.select(
        "Action sur les evenements ?",
        choices=["Lister", "Creer", "Modifier", "Retour"],
    ).ask()

    if action is None or action == "Retour":
        return

    if action == "Lister":
        _call_command("event-list")
    elif action == "Creer":
        _call_command("event-create")
    elif action == "Modifier":
        _call_command("event-update")


def _menu_auth():
    action = questionary.select(
        "Action d'authentification ?",
        choices=["Se connecter", "Se deconnecter", "S'inscrire", "Retour"],
    ).ask()

    if action is None or action == "Retour":
        return

    if action == "Se connecter":
        _call_command("login")
    elif action == "Se deconnecter":
        _call_command("logout")
    elif action == "S'inscrire":
        _call_command("register")


def _call_command(name, **kwargs):
    """Appelle une commande en demandant les parametres manquants."""
    command = _find_command(name)
    if command is None:
        console.print(f"[red]Commande inconnue : {name}[/red]")
        return

    sig = inspect.signature(command.callback)

    for param_name, param in sig.parameters.items():
        if param_name in kwargs:
            continue

        default = param.default

        if isinstance(default, typer.models.OptionInfo):
            prompt_text = default.prompt or param_name
            hide = getattr(default, "hide_input", False)
            value = _ask_param(prompt_text, hide)
            if value is None:
                console.print("[yellow]Annule.[/yellow]")
                return
            kwargs[param_name] = value

    try:
        command.callback(**kwargs)
    except SystemExit:
        pass
    except Exception as e:
        console.print(f"[red]Erreur : {e}[/red]")


def _ask_param(prompt_text, hide=False):
    """Demande une valeur a l'utilisateur."""
    if hide:
        return questionary.password(prompt_text).ask()
    return questionary.text(prompt_text).ask()


def _find_command(name):
    """Trouve une commande Typer par son nom."""
    for cmd in app.registered_commands:
        cmd_name = cmd.name or cmd.callback.__name__
        if cmd_name == name:
            return cmd
    return None
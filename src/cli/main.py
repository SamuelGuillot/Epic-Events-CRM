import typer
from src.config.database import SessionLocal
from src.services.auth import AuthService
from src.cli.display import display_register_result, display_login_result
from src.services.security import clear_token
from datetime import date
from src.services.client import ClientService
from src.cli.display import display_clients, display_client_result

app = typer.Typer(help="Epic Events CRM")


@app.command()
def register(
    full_name: str = typer.Option(..., prompt="Nom complet"),
    email: str = typer.Option(..., prompt="Email"),
    password: str = typer.Option(
        ..., prompt="Mot de passe", hide_input=True, confirmation_prompt=True
    ),
    department: str = typer.Option(..., prompt="Departement"),
):
    """Creer un nouveau compte collaborateur."""
    with SessionLocal() as session:
        service = AuthService(session)
        result = service.register(full_name, email, password, department)
        display_register_result(result)


@app.command()
def login(
    email: str = typer.Option(..., prompt="Email"),
    password: str = typer.Option(..., prompt="Mot de passe", hide_input=True),
):
    """Se connecter au CRM."""
    with SessionLocal() as session:
        service = AuthService(session)
        result = service.login(email, password)
        display_login_result(result)


@app.command()
def logout():
    """Se deconnecter (supprime le token stocke)."""
    if clear_token():
        typer.echo("Deconnexion reussie.")
    else:
        typer.echo("Vous n'etiez pas connecte(e).")

client_app = typer.Typer(help="Commandes de gestion des clients.")
app.add_typer(client_app, name="client")

@client_app.command("list")
def client_list():
    """Afficher la liste de tous les clients."""
    with SessionLocal() as session:
        service = ClientService(session)
        clients = service.list_clients()
        display_clients(clients)

@client_app.command("create")
def client_create(
    full_name: str = typer.Option(..., prompt="Nom complet"),
    email: str = typer.Option(..., prompt="Email"),
    phone: str = typer.Option("", prompt="Telephone (optionnel)"),
    company_name: str = typer.Option("", prompt="Societe (optionnel)"),
):
    """Creer un nouveau client."""
    with SessionLocal() as session:
        auth_service = AuthService(session)
        current_user = auth_service.get_current_user()

        if not current_user:
            typer.echo("Vous n'etes pas connecte(e). Utilisez 'login' d'abord.")
            return

        client_service = ClientService(session)
        result = client_service.create_client(
            full_name=full_name,
            email=email,
            phone=phone or None,
            company_name=company_name or None,
            first_contact_date=date.today(),
            current_user=current_user,
        )
        display_client_result(result)
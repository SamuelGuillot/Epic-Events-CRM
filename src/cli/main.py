import typer
from datetime import date

from src.config.database import SessionLocal
from src.services.auth import AuthService
from src.services.client import ClientService
from src.services.contract import ContractService
from src.inputs.user import RegisterData, LoginData
from src.inputs.client import ClientCreateData
from src.inputs.contract import ContractCreateData
from src.exceptions import EpicEventsError
from src.cli.display import (
    display_user,
    display_clients,
    display_client,
    display_contracts,
    display_contract,
    display_error,
)
from src.services.security import clear_token, create_jwt


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
    data = RegisterData(
        full_name=full_name,
        email=email,
        password=password,
        department=department,
    )

    with SessionLocal() as session:
        try:
            service = AuthService(session)
            user = service.register(data)
            token = create_jwt(user.id, user.email)
            display_user(user)
            typer.echo(f"JWT : {token}")
        except EpicEventsError as e:
            display_error(e.message)


@app.command()
def login(
    email: str = typer.Option(..., prompt="Email"),
    password: str = typer.Option(..., prompt="Mot de passe", hide_input=True),
):
    """Se connecter au CRM."""
    data = LoginData(email=email, password=password)

    with SessionLocal() as session:
        try:
            service = AuthService(session)
            user = service.login(data)
            token = create_jwt(user.id, user.email)
            typer.echo(f"Connexion reussie, bienvenue {user.full_name} !")
            typer.echo(f"JWT : {token}")
        except EpicEventsError as e:
            display_error(e.message)


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
    data = ClientCreateData(
        full_name=full_name,
        email=email,
        phone=phone or None,
        company_name=company_name or None,
        first_contact_date=date.today(),
    )

    with SessionLocal() as session:
        try:
            auth_service = AuthService(session)
            current_user = auth_service.get_current_user()

            service = ClientService(session)
            client = service.create_client(data, current_user)
            display_client(client)
        except EpicEventsError as e:
            display_error(e.message)


contract_app = typer.Typer(help="Commandes de gestion des contrats.")
app.add_typer(contract_app, name="contract")


@contract_app.command("create")
def contract_create(
    client_id: int = typer.Option(..., prompt="ID du client"),
    total_amount: float = typer.Option(..., prompt="Montant total"),
    remaining_amount: float = typer.Option(..., prompt="Montant restant a payer"),
):
    data = ContractCreateData(
        client_id=client_id,
        total_amount=total_amount,
        remaining_amount=remaining_amount,
        creation_date=date.today(),
    )

    with SessionLocal() as session:
        try:
            auth_service = AuthService(session)
            current_user = auth_service.get_current_user()

            service = ContractService(session)
            contract = service.create_contract(data, current_user)
            display_contract(contract)
        except EpicEventsError as e:
            display_error(e.message)


@contract_app.command("list")
def contract_list():
    with SessionLocal() as session:
        service = ContractService(session)
        contracts = service.list_contracts()
        display_contracts(contracts)


if __name__ == "__main__":
    app()
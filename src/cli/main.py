import typer
from datetime import date, datetime

from src.config.database import SessionLocal
from src.services.auth import AuthService
from src.services.client import ClientService
from src.services.contract import ContractService
from src.inputs.user import RegisterData, LoginData
from src.inputs.client import ClientCreateData
from src.inputs.contract import ContractCreateData, ContractUpdateData
from src.exceptions import EpicEventsError
from src.services.event import EventService
from src.inputs.event import EventCreateData, EventUpdateData
from src.cli.display import (
    display_user,
    display_clients,
    display_client,
    display_contracts,
    display_contract,
    display_error,
    display_events, 
    display_event,
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


@app.command("client-list")
def client_list():
    """Afficher la liste de tous les clients."""
    with SessionLocal() as session:
        service = ClientService(session)
        clients = service.list_clients()
        display_clients(clients)


@app.command("client-create")
def client_create(
    full_name: str = typer.Option(..., prompt="Nom complet"),
    email: str = typer.Option(..., prompt="Email"),
    phone: str = typer.Option("", prompt="Telephone (optionnel)"),
    company_name: str = typer.Option("", prompt="Societe (optionnel)"),
):
    """Creer un nouveau client."""
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


@app.command("contract-list")
def contract_list():
    with SessionLocal() as session:
        service = ContractService(session)
        contracts = service.list_contracts()
        display_contracts(contracts)


@app.command("contract-create")
def contract_create(
    client_id: int = typer.Option(..., prompt="ID du client"),
):
    """Creer un nouveau contrat pour un client."""
    with SessionLocal() as session:
        try:
            auth_service = AuthService(session)
            current_user = auth_service.get_current_user()

            client_service = ClientService(session)
            client = client_service.get_client(client_id)

            total_amount = typer.prompt("Montant total", type=float)
            remaining_amount = typer.prompt("Montant restant a payer", type=float)

            data = ContractCreateData(
                client_id=client.id,
                total_amount=total_amount,
                remaining_amount=remaining_amount,
                creation_date=date.today(),
            )

            contract_service = ContractService(session)
            contract = contract_service.create_contract(data, current_user)
            display_contract(contract)
        except EpicEventsError as e:
            display_error(e.message)

@app.command("contract-update")
def contract_update(
    contract_id: int = typer.Option(..., prompt="ID du contrat"),
    sign: bool = typer.Option(False, "--sign", help="Signer le contrat."),
    total_amount: float = typer.Option(None, "--total", help="Nouveau montant total."),
    remaining_amount: float = typer.Option(None, "--remaining", help="Nouveau montant restant."),
):
    data = ContractUpdateData(
        total_amount=total_amount,
        remaining_amount=remaining_amount,
        status=True if sign else None,
    )

    with SessionLocal() as session:
        try:
            service = ContractService(session)
            contract = service.update_contract(contract_id, data)
            display_contract(contract)
        except EpicEventsError as e:
            display_error(e.message)


@app.command("event-list")
def event_list():
    with SessionLocal() as session:
        service = EventService(session)
        events = service.list_events()
        display_events(events)


@app.command("event-create")
def event_create(
    contract_id: int = typer.Option(..., prompt="ID du contrat"),
):
    """Creer un evenement pour un contrat signe."""
    with SessionLocal() as session:
        try:
            auth_service = AuthService(session)
            current_user = auth_service.get_current_user()

            contract_service = ContractService(session)
            contract = contract_service.get_contract(contract_id)

            if not contract.status:
                display_error("Le contrat doit etre signe pour creer un evenement.")
                return

            event_service = EventService(session)
            existing = event_service.get_event_by_contract(contract.id)
            if existing:
                display_error(f"Ce contrat a deja un evenement (ID {existing.id}).")
                return

            event_name = typer.prompt("Nom de l'evenement")
            date_start = typer.prompt("Date de debut (YYYY-MM-DD HH:MM)")
            date_end = typer.prompt("Date de fin (YYYY-MM-DD HH:MM)")
            location = typer.prompt("Lieu (optionnel)", default="")
            attendees_count = typer.prompt("Nombre de participants", default=0, type=int)
            notes = typer.prompt("Notes (optionnel)", default="")

            try:
                parsed_start = datetime.strptime(date_start, "%Y-%m-%d %H:%M")
                parsed_end = datetime.strptime(date_end, "%Y-%m-%d %H:%M")
            except ValueError:
                display_error("Format de date invalide. Utiliser : YYYY-MM-DD HH:MM")
                return

            data = EventCreateData(
                contract_id=contract.id,
                event_name=event_name,
                event_date_start=parsed_start,
                event_date_end=parsed_end,
                location=location or None,
                attendees_count=attendees_count,
                notes=notes or None,
            )

            event = event_service.create_event(data, current_user)
            display_event(event)
        except EpicEventsError as e:
            display_error(e.message)


@app.command("event-update")
def event_update(
    event_id: int = typer.Option(..., prompt="ID de l'evenement"),
    name: str = typer.Option(None, "--name", help="Nouveau nom."),
    location: str = typer.Option(None, "--location", help="Nouveau lieu."),
    attendees: int = typer.Option(None, "--attendees", help="Nouveau nombre de participants."),
    notes: str = typer.Option(None, "--notes", help="Nouvelles notes."),
    support_id: int = typer.Option(None, "--support", help="ID du support a assigner."),
):
    data = EventUpdateData(
        event_name=name,
        location=location,
        attendees_count=attendees,
        notes=notes,
        support_contact_id=support_id,
    )

    with SessionLocal() as session:
        try:
            service = EventService(session)
            event = service.update_event(event_id, data)
            display_event(event)
        except EpicEventsError as e:
            display_error(e.message)


if __name__ == "__main__":
    app()
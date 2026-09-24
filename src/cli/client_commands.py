import typer
from datetime import date

from src.cli.app import app
from src.config.database import SessionLocal
from src.services.auth import AuthService
from src.services.client import ClientService
from src.inputs.client import ClientCreateData, ClientUpdateData
from src.permissions import can_create_client, can_update_client
from src.exceptions import EpicEventsError, PermissionDeniedError
from src.cli.display import display_clients, display_client, display_error


@app.command("client-list")
def client_list():
    """Afficher la liste de tous les clients."""
    with SessionLocal() as session:
        service = ClientService(session)
        clients = service.list_clients()
        display_clients(clients)


@app.command("client-create")
def client_create():
    """Creer un nouveau client."""
    with SessionLocal() as session:
        try:
            auth_service = AuthService(session)
            current_user = auth_service.get_current_user()

            if not can_create_client(current_user):
                raise PermissionDeniedError("Seul un commercial peut creer un client.")

            full_name = typer.prompt("Nom complet")
            email = typer.prompt("Email")
            phone = typer.prompt("Telephone (optionnel)", default="")
            company_name = typer.prompt("Societe (optionnel)", default="")

            data = ClientCreateData(
                full_name=full_name,
                email=email,
                phone=phone or None,
                company_name=company_name or None,
                first_contact_date=date.today(),
            )

            service = ClientService(session)
            client = service.create_client(data, current_user)
            display_client(client)
        except EpicEventsError as e:
            display_error(e.message)


@app.command("client-update")
def client_update(
    client_id: int = typer.Option(..., prompt="ID du client"),
):
    """Mettre a jour un client."""
    with SessionLocal() as session:
        try:
            auth_service = AuthService(session)
            current_user = auth_service.get_current_user()

            client_service = ClientService(session)
            client = client_service.get_client(client_id)

            if not can_update_client(current_user, client):
                raise PermissionDeniedError(
                    "Vous ne pouvez modifier que vos propres clients."
                )

            name = typer.prompt("Nouveau nom (vide pour ne pas changer)", default="")
            email = typer.prompt("Nouvel email (vide pour ne pas changer)", default="")
            phone = typer.prompt("Nouveau telephone (vide pour ne pas changer)", default="")
            company = typer.prompt("Nouvelle societe (vide pour ne pas changer)", default="")

            data = ClientUpdateData(
                full_name=name or None,
                email=email or None,
                phone=phone or None,
                company_name=company or None,
            )

            client = client_service.update_client(client_id, data, current_user)
            display_client(client)
        except EpicEventsError as e:
            display_error(e.message)
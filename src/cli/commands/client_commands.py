from datetime import date

import typer

from src.cli.app import app
from src.cli.decorators import (
    has_object_permission,
    has_permission,
)
from src.cli.displays.client_display import (
    display_client,
    display_clients,
)
from src.cli.displays.error_display import display_error
from src.config.database import SessionLocal
from src.config.sentry import log_error
from src.DTO.client import ClientCreateData, ClientUpdateData
from src.exceptions import EpicEventsError
from src.permissions import can_create_client, can_update_client
from src.services.client import ClientService


def fetch_client(session, client_id, **kwargs):
    """Recupere un client par son ID (appele par le decorateur)."""
    service = ClientService(session)
    return service.get_client(client_id)


@app.command("client-list")
def client_list():
    """Afficher la liste de tous les clients."""
    with SessionLocal() as session:
        try:
            service = ClientService(session)
            clients = service.list_clients()
        except EpicEventsError as e:
            display_error(e)
            return
        except Exception as e:
            log_error(e)
            display_error(e)
            return

        display_clients(clients)


@app.command("client-create")
@has_permission(can_create_client, "creer un client")
def client_create(current_user, session):
    """Creer un nouveau client."""
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


@app.command("client-update")
@has_object_permission(
    can_update_client,
    fetch_client,
    "modifier ce client",
)
def client_update(
    current_user,
    session,
    object,
    client_id: int = typer.Option(
        ..., prompt="ID du client"
    ),
):
    """Mettre a jour un client."""
    name = typer.prompt(
        "Nouveau nom (vide pour ne pas changer)", default=""
    )
    email = typer.prompt(
        "Nouvel email (vide pour ne pas changer)", default=""
    )
    phone = typer.prompt(
        "Nouveau telephone (vide pour ne pas changer)", default=""
    )
    company = typer.prompt(
        "Nouvelle societe (vide pour ne pas changer)", default=""
    )

    data = ClientUpdateData(
        full_name=name or None,
        email=email or None,
        phone=phone or None,
        company_name=company or None,
    )

    service = ClientService(session)
    client = service.update_client(client_id, data, current_user)
    display_client(client)

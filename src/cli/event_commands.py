import typer
from datetime import datetime

from src.cli.app import app
from src.config.database import SessionLocal
from src.services.auth import AuthService
from src.services.contract import ContractService
from src.services.event import EventService
from src.inputs.event import EventCreateData, EventUpdateData
from src.exceptions import EpicEventsError
from src.cli.display import display_events, display_event, display_error


@app.command("event-list")
def event_list():
    """Afficher la liste de tous les evenements."""
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
):
    """Mettre a jour un evenement."""
    with SessionLocal() as session:
        try:
            event_service = EventService(session)
            event = event_service.get_event(event_id)

            name = typer.prompt("Nouveau nom (vide pour ne pas changer)", default="")
            location = typer.prompt("Nouveau lieu (vide pour ne pas changer)", default="")
            attendees = typer.prompt("Nouveau nombre de participants (vide pour ne pas changer)", default="")
            notes = typer.prompt("Nouvelles notes (vide pour ne pas changer)", default="")
            support_id = typer.prompt("ID du support (vide pour ne pas changer)", default="")

            data = EventUpdateData(
                event_name=name or None,
                location=location or None,
                attendees_count=int(attendees) if attendees else None,
                notes=notes or None,
                support_contact_id=int(support_id) if support_id else None,
            )

            event = event_service.update_event(event_id, data)
            display_event(event)
        except EpicEventsError as e:
            display_error(e.message)
import typer
from datetime import datetime

from src.cli.app import app
from src.cli.decorators import has_object_permission
from src.config.database import SessionLocal
from src.services.security.auth import AuthService
from src.services.event import EventService
from src.DTO.event import EventCreateData, EventUpdateData
from src.permissions import can_update_event, can_assign_support
from src.exceptions import (
    EpicEventsError,
    PermissionDeniedError,
    ValidationError,
)
from src.cli.displays.event_display import display_events, display_event
from src.cli.displays.error_display import display_error


def fetch_event(session, event_id, **kwargs):
    """Recupere un evenement par son ID (appele par le decorateur)."""
    service = EventService(session)
    return service.get_event(event_id)


@app.command("event-list")
def event_list():
    """Afficher la liste de tous les evenements."""
    with SessionLocal() as session:
        try:
            service = EventService(session)
            events = service.list_events()
        except EpicEventsError as e:
            display_error(e)
            return

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
                raise ValidationError(
                    "date",
                    "format invalide. Utiliser YYYY-MM-DD HH:MM",
                )

            data = EventCreateData(
                contract_id=contract_id,
                event_name=event_name,
                event_date_start=parsed_start,
                event_date_end=parsed_end,
                location=location or None,
                attendees_count=attendees_count,
                notes=notes or None,
            )

            event_service = EventService(session)
            event = event_service.create_event(data, current_user)

        except EpicEventsError as e:
            display_error(e)
            return

        display_event(event)


@app.command("event-update")
@has_object_permission(can_update_event, fetch_event, "modifier cet evenement")
def event_update(
    current_user,
    session,
    object,
    event_id: int = typer.Option(..., prompt="ID de l'evenement"),
):
    """Mettre a jour un evenement."""
    try:
        name = typer.prompt("Nouveau nom (vide pour ne pas changer)", default="")
        location = typer.prompt("Nouveau lieu (vide pour ne pas changer)", default="")
        attendees = typer.prompt(
            "Nouveau nombre de participants (vide pour ne pas changer)",
            default="",
        )
        notes = typer.prompt("Nouvelles notes (vide pour ne pas changer)", default="")
        support_id = typer.prompt(
            "ID du support (vide pour ne pas changer)", default=""
        )

        if support_id and not can_assign_support(current_user):
            raise PermissionDeniedError("assigner un support")

        data = EventUpdateData(
            event_name=name or None,
            location=location or None,
            attendees_count=int(attendees) if attendees else None,
            notes=notes or None,
            support_contact_id=int(support_id) if support_id else None,
        )

        event_service = EventService(session)
        event = event_service.update_event(event_id, data, current_user)

    except EpicEventsError as e:
        display_error(e)
        return

    display_event(event)
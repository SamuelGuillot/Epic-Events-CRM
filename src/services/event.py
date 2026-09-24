from src.repositories.event_repository import EventRepository
from src.repositories.contract_repository import ContractRepository
from src.inputs.event import EventCreateData, EventUpdateData
from src.exceptions import (
    ContractNotFoundError,
    EventNotFoundError,
    ValidationError,
)


class EventService:
    def __init__(self, session):
        self.event_repo = EventRepository(session)
        self.contract_repo = ContractRepository(session)

    def list_events(self):
        return self.event_repo.get_all()

    def get_event(self, event_id):
        event = self.event_repo.get_by_id(event_id)
        if not event:
            raise EventNotFoundError(f"Evenement ID {event_id} introuvable.")
        return event

    def get_event_by_contract(self, contract_id):
        return self.event_repo.get_by_contract(contract_id)

    def list_by_support(self, support_id):
        return self.event_repo.get_by_support(support_id)

    def list_without_support(self):
        return self.event_repo.get_without_support()

    def create_event(self, data: EventCreateData, current_user):
        data.validate()

        contract = self.contract_repo.get_by_id(data.contract_id)
        if not contract:
            raise ContractNotFoundError(
                f"Contrat ID {data.contract_id} introuvable."
            )

        if not contract.status:
            raise ValidationError(
                "Le contrat doit etre signe pour creer un evenement."
            )

        existing = self.event_repo.get_by_contract(contract.id)
        if existing:
            raise ValidationError(
                f"Ce contrat a deja un evenement (ID {existing.id})."
            )

        return self.event_repo.add_event(data, contract.client_id)

    def update_event(self, event_id, data: EventUpdateData):
        event = self.get_event(event_id)

        if data.event_name is not None:
            event.event_name = data.event_name
        if data.location is not None:
            event.location = data.location
        if data.attendees_count is not None:
            event.attendees_count = data.attendees_count
        if data.notes is not None:
            event.notes = data.notes
        if data.support_contact_id is not None:
            event.support_contact_id = data.support_contact_id

        return self.event_repo.update_event(event)
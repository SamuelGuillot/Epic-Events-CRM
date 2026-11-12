from src.DTO.event import EventCreateData, EventUpdateData
from src.exceptions import (
    ContractNotFoundError,
    ContractNotSignedError,
    EventAlreadyExistsError,
    EventNotFoundError,
    PermissionDeniedError,
)
from src.permissions import can_update_event
from src.repositories.contract_repository import ContractRepository
from src.repositories.event_repository import EventRepository


class EventService:
    def __init__(self, session):
        self.event_repo = EventRepository(session)
        self.contract_repo = ContractRepository(session)

    def list_events(self):
        return self.event_repo.get_all()

    def get_event(self, event_id):
        event = self.event_repo.get_by_id(event_id)
        if not event:
            raise EventNotFoundError(event_id)
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
            raise ContractNotFoundError(data.contract_id)

        if not contract.status:
            raise ContractNotSignedError(contract.id)

        existing = self.event_repo.get_by_contract(contract.id)
        if existing:
            raise EventAlreadyExistsError(contract.id, existing.id)

        data.client_id = contract.client_id
        return self.event_repo.add_event(data)

    def update_event(self, event_id, data: EventUpdateData, current_user):
        event = self.get_event(event_id)

        if not can_update_event(current_user, event):
            raise PermissionDeniedError("modifier cet evenement")

        return self.event_repo.update_event(event_id, data)

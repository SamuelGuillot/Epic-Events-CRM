from dataclasses import dataclass
from datetime import datetime
from src.exceptions import ValidationError


@dataclass
class EventCreateData:
    contract_id: int
    event_name: str
    event_date_start: datetime
    event_date_end: datetime
    location: str = None
    attendees_count: int = 0
    notes: str = None
    client_id: int = None

    def validate(self):
        if self.contract_id is None:
            raise ValidationError("L'ID du contrat est obligatoire.")
        if not self.event_name or not self.event_name.strip():
            raise ValidationError("Le nom de l'evenement est obligatoire.")
        if self.event_date_start is None:
            raise ValidationError("La date de debut est obligatoire.")
        if self.event_date_end is None:
            raise ValidationError("La date de fin est obligatoire.")
        if self.event_date_end < self.event_date_start:
            raise ValidationError(
                "La date de fin ne peut pas etre avant la date de debut."
            )
        if self.attendees_count is not None and self.attendees_count < 0:
            raise ValidationError("Le nombre de participants ne peut pas etre negatif.")


@dataclass
class EventUpdateData:
    event_name: str = None
    location: str = None
    attendees_count: int = None
    notes: str = None
    support_contact_id: int = None


@dataclass
class EventRead:
    id: int
    event_name: str
    event_date_start: datetime
    event_date_end: datetime
    location: str
    attendees_count: int
    notes: str
    contract_id: int
    client_name: str
    support_name: str

    @classmethod
    def from_model(cls, event):
        return cls(
            id=event.id,
            event_name=event.event_name,
            event_date_start=event.event_date_start,
            event_date_end=event.event_date_end,
            location=event.location,
            attendees_count=event.attendees_count,
            notes=event.notes,
            contract_id=event.contract_id,
            client_name=(
                event.client.full_name
                if event.client
                else "Inconnu"
            ),
            support_name=(
                event.support_contact.full_name
                if event.support_contact
                else "Non assigne"
            ),
        )
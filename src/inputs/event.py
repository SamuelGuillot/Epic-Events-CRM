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
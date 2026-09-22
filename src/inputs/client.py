from dataclasses import dataclass
from datetime import date
from src.exceptions import ValidationError


@dataclass
class ClientCreateData:
    full_name: str
    email: str
    phone: str = None
    company_name: str = None
    first_contact_date: date = None

    def validate(self):
        if not self.full_name or not self.full_name.strip():
            raise ValidationError("Le nom complet est obligatoire.")

        if not self.email or "@" not in self.email:
            raise ValidationError("L'email est invalide.")

        if self.first_contact_date is None:
            raise ValidationError("La date de premier contact est obligatoire.")
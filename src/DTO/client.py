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
            raise ValidationError("full_name", "obligatoire")
        if not self.email or "@" not in self.email:
            raise ValidationError("email", "format invalide")
        if self.first_contact_date is None:
            raise ValidationError("first_contact_date", "obligatoire")


@dataclass
class ClientUpdateData:
    full_name: str = None
    email: str = None
    phone: str = None
    company_name: str = None

    def validate(self):
        if self.full_name is not None and not self.full_name.strip():
            raise ValidationError("Le nom complet ne peut pas etre vide.")
        if self.email is not None and "@" not in self.email:
            raise ValidationError("L'email est invalide.")


@dataclass
class ClientRead:
    id: int
    full_name: str
    email: str
    phone: str
    company_name: str
    first_contact_date: date
    commercial_contact_id: int
    commercial_name: str

    @classmethod
    def from_model(cls, client):
        return cls(
            id=client.id,
            full_name=client.full_name,
            email=client.email,
            phone=client.phone,
            company_name=client.company_name,
            first_contact_date=client.first_contact_date,
            commercial_contact_id=client.commercial_contact_id,
            commercial_name=(
                client.commercial_contact.full_name
                if client.commercial_contact
                else "Non assigne"
            ),
        )
from dataclasses import dataclass
from datetime import date

from src.exceptions import ValidationError


@dataclass
class ContractCreateData:
    client_id: int
    total_amount: float
    remaining_amount: float
    creation_date: date = None

    def validate(self):
        if self.client_id is None:
            raise ValidationError("client_id", "obligatoire")
        if self.total_amount is None or self.total_amount <= 0:
            raise ValidationError("total_amount", "doit etre positif")
        if self.remaining_amount is None or self.remaining_amount < 0:
            raise ValidationError(
                "remaining_amount", "ne peut pas etre negatif"
            )
        if self.remaining_amount > self.total_amount:
            raise ValidationError(
                "remaining_amount",
                "ne peut pas depasser le total",
            )
        if self.creation_date is None:
            raise ValidationError("creation_date", "obligatoire")


@dataclass
class ContractUpdateData:
    total_amount: float = None
    remaining_amount: float = None
    status: bool = None


@dataclass
class ContractRead:
    id: int
    client_id: int
    client_name: str
    commercial_contact_id: int
    total_amount: float
    remaining_amount: float
    creation_date: date
    status: bool

    @classmethod
    def from_model(cls, contract):
        return cls(
            id=contract.id,
            client_id=contract.client_id,
            client_name=(
                contract.client.full_name if contract.client else "Inconnu"
            ),
            commercial_contact_id=(
                contract.client.commercial_contact_id
                if contract.client
                else None
            ),
            total_amount=contract.total_amount,
            remaining_amount=contract.remaining_amount,
            creation_date=contract.creation_date,
            status=contract.status,
        )

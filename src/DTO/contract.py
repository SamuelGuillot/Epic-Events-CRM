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
            raise ValidationError("L'ID du client est obligatoire.")
        if self.total_amount is None or self.total_amount <= 0:
            raise ValidationError("Le montant total doit etre positif.")
        if self.remaining_amount is None or self.remaining_amount < 0:
            raise ValidationError("Le montant restant ne peut pas etre negatif.")
        if self.remaining_amount > self.total_amount:
            raise ValidationError("Le montant restant ne peut pas depasser le total.")
        if self.creation_date is None:
            raise ValidationError("La date de creation est obligatoire.")


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
                contract.client.full_name
                if contract.client
                else "Inconnu"
            ),
            total_amount=contract.total_amount,
            remaining_amount=contract.remaining_amount,
            creation_date=contract.creation_date,
            status=contract.status,
        )
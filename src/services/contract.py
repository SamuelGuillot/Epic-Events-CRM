from src.repositories.contract_repository import ContractRepository
from src.repositories.client_repository import ClientRepository
from src.DTO.contract import ContractCreateData, ContractUpdateData
from src.permissions import can_create_contract, can_update_contract
from src.exceptions import (
    ClientNotFoundError,
    ContractNotFoundError,
    PermissionDeniedError,
    ValidationError,
)


class ContractService:
    def __init__(self, session):
        self.contract_repo = ContractRepository(session)
        self.client_repo = ClientRepository(session)

    def list_contracts(self):
        return self.contract_repo.get_all()

    def get_contract(self, contract_id):
        contract = self.contract_repo.get_by_id(contract_id)
        if not contract:
            raise ContractNotFoundError(f"Contrat ID {contract_id} introuvable.")
        return contract

    def list_by_client(self, client_id):
        return self.contract_repo.get_by_client(client_id)

    def create_contract(self, data: ContractCreateData, current_user):
        if not can_create_contract(current_user):
            raise PermissionDeniedError(
                "Seul le departement gestion peut creer un contrat."
            )

        data.validate()

        client = self.client_repo.get_by_id(data.client_id)
        if not client:
            raise ClientNotFoundError(f"Client ID {data.client_id} introuvable.")

        return self.contract_repo.add_contract(data, current_user.id)

    def update_contract(self, contract_id, data: ContractUpdateData, current_user):
        contract = self.get_contract(contract_id)

        if not can_update_contract(current_user, contract):
            raise PermissionDeniedError(
                "Vous ne pouvez pas modifier ce contrat."
            )

        total = data.total_amount if data.total_amount is not None else contract.total_amount
        remaining = data.remaining_amount if data.remaining_amount is not None else contract.remaining_amount

        if remaining < 0:
            raise ValidationError("Le montant restant ne peut pas etre negatif.")
        if remaining > total:
            raise ValidationError("Le montant restant ne peut pas depasser le total.")

        return self.contract_repo.update_contract(contract_id, data)
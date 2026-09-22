from dataclasses import dataclass
from src.models.contract import Contract
from src.repositories.contract_repository import ContractRepository
from src.repositories.client_repository import ClientRepository


@dataclass
class ContractResult:
    success: bool
    message: str
    contract: Contract = None


class ContractService:
    def __init__(self, session):
        self.contract_repo = ContractRepository(session)
        self.client_repo = ClientRepository(session)

    def list_contracts(self):
        return self.contract_repo.get_all()

    def get_contract(self, contract_id):
        return self.contract_repo.get_by_id(contract_id)

    def list_by_client(self, client_id):
        return self.contract_repo.get_by_client(client_id)

    def create_contract(self, client_id, total_amount, remaining_amount, creation_date, current_user):
        client = self.client_repo.get_by_id(client_id)
        if not client:
            return ContractResult(success=False, message=f"Client ID {client_id} introuvable.")

        error = self.validate_contract(total_amount, remaining_amount)
        if error:
            return error

        contract = Contract(
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            creation_date=creation_date,
            status=False,
            client_id=client_id,
            commercial_contact_id=current_user.id,
        )
        self.contract_repo.save(contract)

        return ContractResult(
            success=True,
            message="Contrat cree avec succes",
            contract=contract,
        )

    def validate_contract(self, total_amount, remaining_amount):
        if total_amount <= 0:
            return ContractResult(success=False, message="Le montant total doit etre positif.")

        if remaining_amount < 0:
            return ContractResult(success=False, message="Le montant restant ne peut pas etre negatif.")

        if remaining_amount > total_amount:
            return ContractResult(success=False, message="Le montant restant ne peut pas depasser le total.")

        return None
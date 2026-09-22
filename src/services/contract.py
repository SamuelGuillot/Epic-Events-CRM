from src.repositories.contract_repository import ContractRepository
from src.repositories.client_repository import ClientRepository
from src.inputs.contract import ContractCreateData
from src.exceptions import ClientNotFoundError, ContractNotFoundError


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
        data.validate()

        client = self.client_repo.get_by_id(data.client_id)
        if not client:
            raise ClientNotFoundError(f"Client ID {data.client_id} introuvable.")

        return self.contract_repo.add_contract(data, current_user.id)
from src.config.sentry import log_info
from src.DTO.contract import (
    ContractCreateData,
    ContractUpdateData,
)
from src.exceptions import (
    ClientNotFoundError,
    ContractNotFoundError,
    PermissionDeniedError,
    ValidationError,
)
from src.permissions import (
    can_create_contract,
    can_sign_contract,
    can_update_contract,
)
from src.repositories.client_repository import ClientRepository
from src.repositories.contract_repository import ContractRepository


class ContractService:
    def __init__(self, session):
        self.contract_repo = ContractRepository(session)
        self.client_repo = ClientRepository(session)

    def list_contracts(self):
        return self.contract_repo.get_all()

    def get_contract(self, contract_id):
        contract = self.contract_repo.get_by_id(contract_id)
        if not contract:
            raise ContractNotFoundError(contract_id)
        return contract

    def list_by_client(self, client_id):
        return self.contract_repo.get_by_client(client_id)

    def create_contract(self, data: ContractCreateData, current_user):
        if not can_create_contract(current_user):
            raise PermissionDeniedError("creer un contrat")

        data.validate()

        client = self.client_repo.get_by_id(data.client_id)
        if not client:
            raise ClientNotFoundError(data.client_id)

        return self.contract_repo.add_contract(
            data, current_user.id
        )

    def update_contract(
        self,
        contract_id,
        data: ContractUpdateData,
        current_user,
    ):
        contract = self.get_contract(contract_id)

        if not can_update_contract(current_user, contract):
            raise PermissionDeniedError("modifier ce contrat")

        if data.status is True and not can_sign_contract(current_user):
            raise PermissionDeniedError("signer un contrat")

        total = (
            data.total_amount
            if data.total_amount is not None
            else contract.total_amount
        )
        remaining = (
            data.remaining_amount
            if data.remaining_amount is not None
            else contract.remaining_amount
        )

        if remaining < 0:
            raise ValidationError(
                "remaining_amount",
                "ne peut pas etre negatif",
            )
        if remaining > total:
            raise ValidationError(
                "remaining_amount",
                "ne peut pas depasser le total",
            )

        was_signed = contract.status
        contract = self.contract_repo.update_contract(
            contract_id, data
        )

        if data.status is True and not was_signed:
            log_info(
                f"Contrat #{contract.id} "
                f"signe par {current_user.email}"
            )

        return contract

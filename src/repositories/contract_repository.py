from src.DTO.contract import ContractRead
from src.models.contract import Contract


class ContractRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        contracts = self.session.query(Contract).order_by(Contract.id).all()
        results = []
        for contract in contracts:
            results.append(ContractRead.from_model(contract))
        return results

    def get_by_id(self, contract_id):
        contract = (
            self.session.query(Contract)
            .filter(Contract.id == contract_id)
            .first()
        )
        if not contract:
            return None
        return ContractRead.from_model(contract)

    def get_by_client(self, client_id):
        contracts = (
            self.session.query(Contract)
            .filter(Contract.client_id == client_id)
            .order_by(Contract.id)
            .all()
        )
        results = []
        for contract in contracts:
            results.append(ContractRead.from_model(contract))
        return results

    def add_contract(self, data, commercial_contact_id):
        contract = Contract(
            total_amount=data.total_amount,
            remaining_amount=data.remaining_amount,
            creation_date=data.creation_date,
            status=False,
            client_id=data.client_id,
            commercial_contact_id=commercial_contact_id,
        )
        self.session.add(contract)
        self.session.commit()
        self.session.refresh(contract)
        return ContractRead.from_model(contract)

    def update_contract(self, contract_id, data):
        contract = (
            self.session.query(Contract)
            .filter(Contract.id == contract_id)
            .first()
        )
        if not contract:
            return None

        if data.total_amount is not None:
            contract.total_amount = data.total_amount
        if data.remaining_amount is not None:
            contract.remaining_amount = data.remaining_amount
        if data.status is not None:
            contract.status = data.status

        self.session.commit()
        self.session.refresh(contract)
        return ContractRead.from_model(contract)

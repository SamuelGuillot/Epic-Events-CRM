from src.models.contract import Contract


class ContractRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Contract).order_by(Contract.id).all()

    def get_by_id(self, contract_id):
        return (
            self.session.query(Contract)
            .filter(Contract.id == contract_id)
            .first()
        )

    def get_by_client(self, client_id):
        return (
            self.session.query(Contract)
            .filter(Contract.client_id == client_id)
            .order_by(Contract.id)
            .all()
        )

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
        return contract
from src.models.contract import Contract


class ContractRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Contract).order_by(Contract.id).all()

    def get_by_id(self, contract_id):
        return self.session.query(Contract).filter(Contract.id == contract_id).first()

    def get_by_client(self, client_id):
        return (
            self.session.query(Contract)
            .filter(Contract.client_id == client_id)
            .order_by(Contract.id)
            .all()
        )

    def save(self, contract):
        self.session.add(contract)
        self.session.commit()
        self.session.refresh(contract)
        return contract
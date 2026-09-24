from src.models.client import Client


class ClientRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Client).order_by(Client.id).all()

    def get_by_id(self, client_id):
        return self.session.query(Client).filter(Client.id == client_id).first()

    def get_by_commercial(self, commercial_id):
        return (
            self.session.query(Client)
            .filter(Client.commercial_contact_id == commercial_id)
            .order_by(Client.id)
            .all()
        )

    def search(self, name):
        return (
            self.session.query(Client)
            .filter(Client.full_name == name)
            .all()
        )

    def add_client(self, data, commercial_contact_id):
        client = Client(
            full_name=data.full_name,
            email=data.email,
            phone=data.phone,
            company_name=data.company_name,
            first_contact_date=data.first_contact_date,
            commercial_contact_id=commercial_contact_id,
        )
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client

    def update_client(self, client):
        self.session.commit()
        self.session.refresh(client)
        return client
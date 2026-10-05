from src.DTO.client import ClientRead
from src.models.client import Client


class ClientRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        clients = self.session.query(Client).order_by(Client.id).all()
        results = []
        for client in clients:
            results.append(ClientRead.from_model(client))
        return results

    def get_by_id(self, client_id):
        client = (
            self.session.query(Client)
            .filter(Client.id == client_id)
            .first()
        )
        if not client:
            return None
        return ClientRead.from_model(client)

    def get_by_commercial(self, commercial_id):
        clients = (
            self.session.query(Client)
            .filter(Client.commercial_contact_id == commercial_id)
            .order_by(Client.id)
            .all()
        )
        results = []
        for client in clients:
            results.append(ClientRead.from_model(client))
        return results

    def search(self, name):
        clients = (
            self.session.query(Client)
            .filter(Client.full_name == name)
            .all()
        )
        results = []
        for client in clients:
            results.append(ClientRead.from_model(client))
        return results

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
        return ClientRead.from_model(client)

    def update_client(self, client_id, data):
        client = (
            self.session.query(Client)
            .filter(Client.id == client_id)
            .first()
        )
        if not client:
            return None

        if data.full_name is not None:
            client.full_name = data.full_name
        if data.email is not None:
            client.email = data.email
        if data.phone is not None:
            client.phone = data.phone
        if data.company_name is not None:
            client.company_name = data.company_name

        self.session.commit()
        self.session.refresh(client)
        return ClientRead.from_model(client)

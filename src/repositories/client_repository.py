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
        return self.session.query(Client).filter(
            Client.full_name == name
        ).all()

    def save(self, client):
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client
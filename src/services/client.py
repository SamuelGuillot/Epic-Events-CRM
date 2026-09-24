from src.repositories.client_repository import ClientRepository
from src.inputs.client import ClientCreateData
from src.exceptions import ClientNotFoundError


class ClientService:
    def __init__(self, session):
        self.client_repo = ClientRepository(session)

    def list_clients(self):
        return self.client_repo.get_all()

    def get_client(self, client_id):
        client = self.client_repo.get_by_id(client_id)
        if not client:
            raise ClientNotFoundError(f"Client ID {client_id} introuvable.")
        return client

    def list_by_commercial(self, commercial_id):
        return self.client_repo.get_by_commercial(commercial_id)

    def search_clients(self, name):
        return self.client_repo.search(name)

    def create_client(self, data: ClientCreateData, current_user):
        data.validate()
        return self.client_repo.add_client(data, current_user.id)

    def update_client(self, client_id, data):
        client = self.get_client(client_id)

        data.validate()

        if data.full_name is not None:
            client.full_name = data.full_name
        if data.email is not None:
            client.email = data.email
        if data.phone is not None:
            client.phone = data.phone
        if data.company_name is not None:
            client.company_name = data.company_name

        return self.client_repo.update_client(client)
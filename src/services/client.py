from src.DTO.client import ClientCreateData, ClientUpdateData
from src.exceptions import ClientNotFoundError, PermissionDeniedError
from src.permissions import can_create_client, can_update_client
from src.repositories.client_repository import ClientRepository


class ClientService:
    def __init__(self, session):
        self.client_repo = ClientRepository(session)

    def list_clients(self):
        return self.client_repo.get_all()

    def get_client(self, client_id):
        client = self.client_repo.get_by_id(client_id)
        if not client:
            raise ClientNotFoundError(client_id)
        return client

    def list_by_commercial(self, commercial_id):
        return self.client_repo.get_by_commercial(commercial_id)

    def search_clients(self, name):
        return self.client_repo.search(name)

    def create_client(self, data: ClientCreateData, current_user):
        if not can_create_client(current_user):
            raise PermissionDeniedError("creer un client")

        data.validate()
        return self.client_repo.add_client(data, current_user.id)

    def update_client(self, client_id, data: ClientUpdateData, current_user):
        client = self.get_client(client_id)

        if not can_update_client(current_user, client):
            raise PermissionDeniedError("modifier ce client")

        data.validate()
        return self.client_repo.update_client(client_id, data)

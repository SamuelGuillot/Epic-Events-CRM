from dataclasses import dataclass
from src.models.client import Client
from src.repositories.client_repository import ClientRepository
from src.services.validators import is_valid_email, is_not_empty


@dataclass
class ClientResult:
    success: bool
    message: str
    client: Client = None


class ClientService:
    def __init__(self, session):
        self.client_repo = ClientRepository(session)

    def list_clients(self):
        return self.client_repo.get_all()

    def get_client(self, client_id):
        return self.client_repo.get_by_id(client_id)

    def list_by_commercial(self, commercial_id):
        return self.client_repo.get_by_commercial(commercial_id)

    def search_clients(self, name):
        return self.client_repo.search(name)

    def create_client(self, full_name, email, phone, company_name, first_contact_date, current_user):
        error = self.validate_client(full_name, email)
        if error:
            return error

        client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name,
            first_contact_date=first_contact_date,
            commercial_contact_id=current_user.id,
        )
        self.client_repo.save(client)

        return ClientResult(
            success=True,
            message="Client créé avec succès",
            client=client,
        )

    def validate_client(self, full_name, email):
        if not is_not_empty(full_name):
            return ClientResult(success=False, message="Le nom complet est obligatoire.")

        if not is_valid_email(email):
            return ClientResult(success=False, message="L'email est invalide.")

        return None
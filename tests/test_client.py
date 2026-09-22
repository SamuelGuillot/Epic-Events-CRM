from datetime import date
import pytest
from src.services.client import ClientService
from src.inputs.client import ClientCreateData
from src.exceptions import ValidationError


def build_client_data(**kwargs):
    defaults = {
        "full_name": "Casey Anthony",
        "email": "casey@mail.com",
        "phone": "0606060606",
        "company_name": "Cool Startup",
        "first_contact_date": date(2021, 4, 18),
    }
    defaults.update(kwargs)
    return ClientCreateData(**defaults)


def test_create_client_success(session, sam):
    service = ClientService(session)

    client = service.create_client(build_client_data(), sam)

    assert client is not None
    assert client.full_name == "Casey Anthony"
    assert client.id is not None


def test_create_client_without_name(session, sam):
    service = ClientService(session)

    with pytest.raises(ValidationError):
        service.create_client(build_client_data(full_name=""), sam)


def test_create_client_invalid_email(session, sam):
    service = ClientService(session)

    with pytest.raises(ValidationError):
        service.create_client(build_client_data(email="pas_un_email"), sam)


def test_list_clients_empty(session):
    service = ClientService(session)
    assert service.list_clients() == []


def test_list_clients_with_data(session, sam):
    service = ClientService(session)

    service.create_client(build_client_data(
        full_name="Casey Anthony", email="casey@mail.com",
    ), sam)
    service.create_client(build_client_data(
        full_name="Paul Pogba", email="paul@mail.com",
    ), sam)
    service.create_client(build_client_data(
        full_name="MF Doom", email="doom@mail.com",
    ), sam)

    clients = service.list_clients()
    assert len(clients) == 3
    names = [c.full_name for c in clients]
    assert "Casey Anthony" in names
    assert "Paul Pogba" in names
    assert "MF Doom" in names
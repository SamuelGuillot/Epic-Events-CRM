from datetime import date

import pytest

from src.DTO.client import ClientCreateData, ClientUpdateData
from src.exceptions import (
    ClientNotFoundError,
    PermissionDeniedError,
    ValidationError,
)
from src.services.client import ClientService


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
        service.create_client(
            build_client_data(full_name=""), sam
        )


def test_create_client_invalid_email(session, sam):
    service = ClientService(session)

    with pytest.raises(ValidationError):
        service.create_client(
            build_client_data(email="pas_un_email"), sam
        )


def test_create_client_permission_denied(session, dawn):
    service = ClientService(session)

    with pytest.raises(PermissionDeniedError):
        service.create_client(build_client_data(), dawn)


def test_get_client_success(session, sam, make_client):
    client = make_client(sam)
    service = ClientService(session)

    found = service.get_client(client.id)

    assert found is not None
    assert found.id == client.id


def test_get_client_not_found(session):
    service = ClientService(session)

    with pytest.raises(ClientNotFoundError):
        service.get_client(9999)


def test_list_clients_empty(session):
    service = ClientService(session)

    assert service.list_clients() == []


def test_list_clients_with_data(session, sam):
    service = ClientService(session)

    service.create_client(
        build_client_data(
            full_name="Casey Anthony",
            email="casey@mail.com",
        ),
        sam,
    )
    service.create_client(
        build_client_data(
            full_name="Paul Pogba",
            email="paul@mail.com",
        ),
        sam,
    )
    service.create_client(
        build_client_data(
            full_name="MF Doom",
            email="doom@mail.com",
        ),
        sam,
    )

    clients = service.list_clients()

    assert len(clients) == 3
    names = [c.full_name for c in clients]
    assert "Casey Anthony" in names
    assert "Paul Pogba" in names
    assert "MF Doom" in names


def test_list_by_commercial_empty(session, sam):
    service = ClientService(session)

    assert service.list_by_commercial(sam.id) == []


def test_list_by_commercial_with_data(
    session, sam, ed, make_client
):
    make_client(sam, name="Client Sam")
    make_client(ed, name="Client Ed", email="edclient@mail.com")
    service = ClientService(session)

    clients = service.list_by_commercial(sam.id)

    assert len(clients) == 1
    assert clients[0].full_name == "Client Sam"


def test_search_clients_found(session, sam, make_client):
    make_client(sam, name="Casey Anthony")
    service = ClientService(session)

    results = service.search_clients("Casey Anthony")

    assert len(results) == 1
    assert results[0].full_name == "Casey Anthony"


def test_search_clients_not_found(session, sam, make_client):
    make_client(sam, name="Casey Anthony")
    service = ClientService(session)

    results = service.search_clients("Inconnu")

    assert results == []


def test_update_client_full_name(session, sam, make_client):
    client = make_client(sam)
    service = ClientService(session)

    data = ClientUpdateData(full_name="Nouveau Nom")
    updated = service.update_client(client.id, data, sam)

    assert updated.full_name == "Nouveau Nom"


def test_update_client_email(session, sam, make_client):
    client = make_client(sam)
    service = ClientService(session)

    data = ClientUpdateData(email="nouveau@mail.com")
    updated = service.update_client(client.id, data, sam)

    assert updated.email == "nouveau@mail.com"


def test_update_client_all_fields(session, sam, make_client):
    client = make_client(sam)
    service = ClientService(session)

    data = ClientUpdateData(
        full_name="Nouveau",
        email="nouveau@mail.com",
        phone="0102030405",
        company_name="Nouvelle Societe",
    )
    updated = service.update_client(client.id, data, sam)

    assert updated.full_name == "Nouveau"
    assert updated.email == "nouveau@mail.com"
    assert updated.phone == "0102030405"
    assert updated.company_name == "Nouvelle Societe"


def test_update_client_not_found(session, sam):
    service = ClientService(session)
    data = ClientUpdateData(full_name="Test")

    with pytest.raises(ClientNotFoundError):
        service.update_client(9999, data, sam)


def test_update_client_permission_denied(
    session, sam, ed, make_client
):
    """Un commercial ne peut modifier que ses propres clients."""
    client = make_client(ed, name="Client Ed")
    service = ClientService(session)

    data = ClientUpdateData(full_name="Tentative")

    with pytest.raises(PermissionDeniedError):
        service.update_client(client.id, data, sam)


def test_update_client_invalid_email(session, sam, make_client):
    client = make_client(sam)
    service = ClientService(session)

    data = ClientUpdateData(email="pas_un_email")

    with pytest.raises(ValidationError):
        service.update_client(client.id, data, sam)

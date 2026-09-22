from datetime import date
from src.services.client import ClientService


def test_create_client_succes(session, sam):
    service = ClientService(session)

    result = service.create_client(
        full_name="Casey Anthony",
        email="casey@mail.com",
        phone="0606060606",
        company_name="Cool Startup",
        first_contact_date=date(2021, 4, 18),
        current_user=sam,
    )

    assert result.success is True
    assert result.client is not None
    assert result.client.full_name == "Casey Anthony"
    assert result.client.id is not None


def test_create_client_sans_nom(session, sam):
    service = ClientService(session)

    result = service.create_client(
        full_name="",
        email="casey@mail.com",
        phone=None,
        company_name=None,
        first_contact_date=date(2021, 4, 18),
        current_user=sam,
    )

    assert result.success is False
    assert result.client is None


def test_create_client_email_invalide(session, sam):
    service = ClientService(session)

    result = service.create_client(
        full_name="Casey Anthony",
        email="pas_un_email",
        phone=None,
        company_name=None,
        first_contact_date=date(2021, 4, 18),
        current_user=sam,
    )

    assert result.success is False


def test_list_clients_vide(session):
    service = ClientService(session)
    assert service.list_clients() == []


def test_list_clients_avec_donnees(session, sam):
    service = ClientService(session)

    service.create_client(
        "Casey Anthony", "casey@mail.com", None, "Coolp",
        date(2021, 4, 18), sam,
    )
    service.create_client(
        "Paul Pogba", "paul@mail.com", None, "Footolip",
        date(2022, 5, 10), sam,
    )
    service.create_client(
        "MF Doom", "doom@mail.com", None, "Rapza",
        date(2023, 6, 15), sam,
    )

    clients = service.list_clients()
    assert len(clients) == 3
    noms = [c.full_name for c in clients]
    assert "Casey Anthony" in noms
    assert "Paul Pogba" in noms
    assert "MF Doom" in noms
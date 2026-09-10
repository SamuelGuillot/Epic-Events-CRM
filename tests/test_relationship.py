from datetime import date
from src.models import User, Client


def test_creation_client_avec_relation(session, user_sam):
    client = Client(
        full_name="Casey Anthony",
        email="casey@mail.com",
        phone="+678 123 456 78",
        company_name="Cool Startup LLC",
        first_contact_date=date(2021, 4, 18),
        commercial_contact=user_sam,
    )
    session.add(client)
    session.commit()

    assert client.id is not None
    assert client.full_name == "Casey Anthony"


def test_acces_commercial_depuis_client(session,user_sam):
    client = Client(
        full_name="Casey Anthony",
        email="casey@mail.com",
        first_contact_date=date(2021, 4, 18),
        commercial_contact=user_sam,
    )
    session.add(client)
    session.commit()

    assert client.commercial_contact is not None
    assert client.commercial_contact.full_name == "sam"
    assert client.commercial_contact.email == "sam@mail.com"


def test_acces_clients_depuis_commercial(session, user_sam):
    client1 = Client(
        full_name="Casey Anthony",
        email="casey@mail.com",
        first_contact_date=date(2021, 4, 18),
        commercial_contact=user_sam,
    )
    client2 = Client(
        full_name="Paul Pogba",
        email="paul@mail.com",
        first_contact_date=date(2022, 5, 10),
        commercial_contact=user_sam,
    )
    client3 = Client(
        full_name="MF Doom",
        email="doom@mail.com",
        first_contact_date=date(2023, 6, 15),
        commercial_contact=user_sam,
    )
    session.add_all([client1, client2, client3])
    session.commit()

    assert len(user_sam.clients) == 3
    noms = [c.full_name for c in user_sam.clients]
    assert "Casey Anthony" in noms
    assert "Paul Pogba" in noms
    assert "MF Doom" in noms


def test_commercial_contact_id_est_bien_ecrit(session, user_sam):
    client = Client(
        full_name="Casey Anthony",
        email="casey@mail.com",
        first_contact_date=date(2023, 1, 1),
        commercial_contact=user_sam,
    )
    session.add(client)
    session.commit()

    assert client.commercial_contact_id == user_sam.id


def test_client_sans_commercial(session):
    client = Client(
        full_name="Client Orphelin",
        email="orphan@mail.com",
        first_contact_date=date(2023, 1, 1),
    )
    session.add(client)
    session.commit()

    assert client.commercial_contact_id is None
    assert client.commercial_contact is None
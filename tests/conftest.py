from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.DTO.contract import (
    ContractCreateData,
    ContractUpdateData,
)
from src.models import Base, Client, Department, User
from src.services.contract import ContractService
from src.services.security import hash_password


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()


@pytest.fixture
def sam(session):
    user = User(
        employee_number="EMP001",
        full_name="sam",
        email="sam@mail.com",
        password_hash=hash_password("12345678"),
        department=Department.COMMERCIAL,
    )
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def ed(session):
    user = User(
        employee_number="EMP002",
        full_name="ed",
        email="ed@mail.com",
        password_hash=hash_password("12345678"),
        department=Department.COMMERCIAL,
    )
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def dawn(session):
    user = User(
        employee_number="EMP003",
        full_name="dawn",
        email="dawn@epicevents.com",
        password_hash=hash_password("12345678"),
        department=Department.GESTION,
    )
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def kate(session):
    user = User(
        employee_number="EMP004",
        full_name="kate",
        email="kate@epicevents.com",
        password_hash=hash_password("12345678"),
        department=Department.SUPPORT,
    )
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def make_client(session):
    def _make_client(sam, name="Casey Anthony", email="casey@mail.com"):
        client = Client(
            full_name=name,
            email=email,
            first_contact_date=date(2021, 4, 18),
            commercial_contact=sam,
        )
        session.add(client)
        session.commit()
        return client

    return _make_client


@pytest.fixture
def make_contract(session, dawn):
    def _make_contract(client, signed=False):
        service = ContractService(session)
        data = ContractCreateData(
            client_id=client.id,
            total_amount=5000.0,
            remaining_amount=5000.0,
            creation_date=date(2024, 1, 1),
        )
        contract = service.create_contract(data, dawn)

        if signed:
            update = ContractUpdateData(status=True)
            service.contract_repo.update_contract(contract.id, update)

        return service.get_contract(contract.id)

    return _make_contract


@pytest.fixture
def make_event(session):
    def _make_event(contract, current_user, support=None):
        from datetime import datetime
        from src.DTO.event import (
            EventCreateData,
            EventUpdateData,
        )
        from src.services.event import EventService

        service = EventService(session)
        data = EventCreateData(
            contract_id=contract.id,
            event_name="Test Event",
            event_date_start=datetime(2026, 11, 15, 14, 0),
            event_date_end=datetime(2026, 11, 15, 23, 0),
        )
        event = service.create_event(data, current_user)

        if support:
            update = EventUpdateData(support_contact_id=support.id)
            service.event_repo.update_event(event.id, update)
            event = service.get_event(event.id)

        return event

    return _make_event


@pytest.fixture
def auth_service(session):
    from src.services.security.auth import AuthService

    return AuthService(session)

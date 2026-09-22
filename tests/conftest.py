import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base, User, Client, Department
from src.services.security import hash_password


@pytest.fixture
def session():
    """Crée une base SQLite en mémoire, isolée pour chaque test."""
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
def auth_service(session):
    """Retourne une instance d'AuthService liée à la session de test."""
    from src.services.auth import AuthService
    return AuthService(session)
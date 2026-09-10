import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base, User, Client, Department


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session 

    session.close()


@pytest.fixture
def user_sam(session):
    from src.utils.security import hash_password

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
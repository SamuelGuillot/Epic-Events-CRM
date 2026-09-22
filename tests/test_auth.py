import pytest
from src.models import User, Department
from src.inputs.user import RegisterData, LoginData
from src.exceptions import (
    EmailAlreadyUsedError,
    InvalidCredentialsError,
    InvalidDepartmentError,
    InvalidPasswordError,
)


def test_register_success(auth_service):
    data = RegisterData(
        full_name="Johnny Bravo",
        email="johnny@mail.com",
        password="motdepasse123",
        department="support",
    )

    user = auth_service.register(data)

    assert user is not None
    assert user.email == "johnny@mail.com"
    assert user.full_name == "Johnny Bravo"
    assert user.department == Department.SUPPORT


def test_register_email_already_used(auth_service):
    auth_service.register(RegisterData(
        full_name="Johnny Bravo",
        email="johnny@mail.com",
        password="motdepasse123",
        department="support",
    ))

    with pytest.raises(EmailAlreadyUsedError):
        auth_service.register(RegisterData(
            full_name="Donnie Brasco",
            email="johnny@mail.com",
            password="autremotdepasse",
            department="commercial",
        ))


def test_register_invalid_department(auth_service):
    with pytest.raises(InvalidDepartmentError):
        auth_service.register(RegisterData(
            full_name="Johnny Bravo",
            email="johnny@mail.com",
            password="motdepasse123",
            department="informatique",
        ))


def test_register_password_too_short(auth_service):
    with pytest.raises(InvalidPasswordError):
        auth_service.register(RegisterData(
            full_name="Johnny Bravo",
            email="johnny@mail.com",
            password="court",
            department="support",
        ))


def test_register_password_is_hashed(auth_service, session):
    auth_service.register(RegisterData(
        full_name="Johnny Bravo",
        email="johnny@mail.com",
        password="motdepasse123",
        department="support",
    ))

    user = session.query(User).filter(User.email == "johnny@mail.com").first()

    assert user is not None
    assert user.password_hash != "motdepasse123"
    assert user.password_hash.startswith("$argon2id$")


def test_register_employee_number_auto(auth_service):
    user1 = auth_service.register(RegisterData(
        full_name="Johnny Bravo", email="johnny@mail.com",
        password="motdepasse123", department="support",
    ))
    user2 = auth_service.register(RegisterData(
        full_name="Donnie Brasco", email="donnie@mail.com",
        password="motdepasse123", department="commercial",
    ))

    assert user1.employee_number == "EMP001"
    assert user2.employee_number == "EMP002"


def test_login_success(auth_service):
    auth_service.register(RegisterData(
        full_name="Johnny Bravo",
        email="johnny@mail.com",
        password="motdepasse123",
        department="support",
    ))

    user = auth_service.login(LoginData(
        email="johnny@mail.com",
        password="motdepasse123",
    ))

    assert user is not None
    assert user.email == "johnny@mail.com"


def test_login_unknown_email(auth_service):
    with pytest.raises(InvalidCredentialsError):
        auth_service.login(LoginData(
            email="inconnu@mail.com",
            password="motdepasse123",
        ))


def test_login_wrong_password(auth_service):
    auth_service.register(RegisterData(
        full_name="Johnny Bravo",
        email="johnny@mail.com",
        password="motdepasse123",
        department="support",
    ))

    with pytest.raises(InvalidCredentialsError):
        auth_service.login(LoginData(
            email="johnny@mail.com",
            password="mauvais_mdp",
        ))
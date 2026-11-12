import pytest

from src.DTO.user import (
    LoginData,
    RegisterData,
    UserUpdateData,
)
from src.exceptions import (
    EmailAlreadyUsedError,
    InvalidCredentialsError,
    NotAuthenticatedError,
    UserNotFoundError,
)

def test_update_user_full_name(auth_service, sam):
    data = UserUpdateData(full_name="Samuel")
    user = auth_service.update_user(sam.id, data)

    assert user.full_name == "Samuel"


def test_update_user_email(auth_service, sam):
    data = UserUpdateData(email="nouveau@mail.com")
    user = auth_service.update_user(sam.id, data)

    assert user.email == "nouveau@mail.com"


def test_update_user_department(auth_service, sam):
    data = UserUpdateData(department="gestion")
    user = auth_service.update_user(sam.id, data)

    assert user.department.value == "gestion"


def test_update_user_email_already_used(
    auth_service, sam, dawn
):
    data = UserUpdateData(email=dawn.email)

    with pytest.raises(EmailAlreadyUsedError):
        auth_service.update_user(sam.id, data)


def test_update_user_not_found(auth_service):
    data = UserUpdateData(full_name="Test")

    with pytest.raises(UserNotFoundError):
        auth_service.update_user(9999, data)


def test_update_user_all_fields(auth_service, sam):
    data = UserUpdateData(
        full_name="Samuel",
        email="samuel@mail.com",
        department="gestion",
    )
    user = auth_service.update_user(sam.id, data)

    assert user.full_name == "Samuel"
    assert user.email == "samuel@mail.com"
    assert user.department.value == "gestion"

def test_get_user_success(auth_service, sam):
    user = auth_service.get_user(sam.id)

    assert user is not None
    assert user.id == sam.id


def test_get_user_not_found(auth_service):
    with pytest.raises(UserNotFoundError):
        auth_service.get_user(9999)


def fake_get_token_none():
    return None


def fake_get_token_valid():
    return "token_valide"


def fake_decode_raises(token):
    raise Exception("Invalid token")


def fake_decode_no_user_id(token):
    return {"email": "test@mail.com"}


def fake_decode_user_id_9999(token):
    return {"user_id": 9999}


def test_get_current_user_no_token(
    auth_service, monkeypatch
):
    monkeypatch.setattr(
        "src.services.security.auth.get_token",
        fake_get_token_none,
    )

    with pytest.raises(NotAuthenticatedError):
        auth_service.get_current_user()


def test_get_current_user_invalid_token(
    auth_service, monkeypatch
):
    monkeypatch.setattr(
        "src.services.security.auth.get_token",
        fake_get_token_valid,
    )
    monkeypatch.setattr(
        "src.services.security.auth.decode_jwt",
        fake_decode_raises,
    )

    with pytest.raises(NotAuthenticatedError):
        auth_service.get_current_user()


def test_get_current_user_no_user_id(
    auth_service, monkeypatch
):
    monkeypatch.setattr(
        "src.services.security.auth.get_token",
        fake_get_token_valid,
    )
    monkeypatch.setattr(
        "src.services.security.auth.decode_jwt",
        fake_decode_no_user_id,
    )

    with pytest.raises(NotAuthenticatedError):
        auth_service.get_current_user()


def test_get_current_user_user_not_found(
    auth_service, monkeypatch
):
    monkeypatch.setattr(
        "src.services.security.auth.get_token",
        fake_get_token_valid,
    )
    monkeypatch.setattr(
        "src.services.security.auth.decode_jwt",
        fake_decode_user_id_9999,
    )

    with pytest.raises(NotAuthenticatedError):
        auth_service.get_current_user()


def make_fake_decode_with_user_id(user_id):
    def fake_decode(token):
        return {"user_id": user_id}
    return fake_decode


def test_get_current_user_success(
    auth_service, sam, monkeypatch
):
    monkeypatch.setattr(
        "src.services.security.auth.get_token",
        fake_get_token_valid,
    )

    fake_decode = make_fake_decode_with_user_id(sam.id)
    monkeypatch.setattr(
        "src.services.security.auth.decode_jwt",
        fake_decode,
    )

    user = auth_service.get_current_user()

    assert user is not None
    assert user.id == sam.id

def test_register_creates_user_with_hashed_password(
    auth_service, session
):
    from src.models import User

    data = RegisterData(
        full_name="Johnny Bravo",
        email="johnny@mail.com",
        password="motdepasse123",
        department="commercial",
    )
    auth_service.register(data)

    db_user = (
        session.query(User)
        .filter(User.email == "johnny@mail.com")
        .first()
    )

    assert db_user is not None
    assert db_user.password_hash != "motdepasse123"
    assert db_user.password_hash.startswith("$argon2id$")


def make_fake_save_token(storage):
    def fake_save(token):
        storage["token"] = token
    return fake_save


def test_login_saves_token(auth_service, sam, monkeypatch):
    storage = {}

    fake_save = make_fake_save_token(storage)
    monkeypatch.setattr(
        "src.services.security.auth.save_token",
        fake_save,
    )

    data = LoginData(
        email="sam@mail.com",
        password="12345678",
    )
    auth_service.login(data)

    assert "token" in storage
    assert storage["token"] is not None

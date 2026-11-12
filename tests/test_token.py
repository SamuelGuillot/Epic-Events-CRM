import pytest

from src.services.security.tokens import (
    clear_token,
    create_jwt,
    decode_jwt,
    get_token,
    save_token,
)


def test_create_jwt_returns_token():
    token = create_jwt(1, "sam@mail.com")

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_jwt_success():
    token = create_jwt(1, "sam@mail.com")
    payload = decode_jwt(token)

    assert payload["user_id"] == 1
    assert payload["email"] == "sam@mail.com"
    assert "exp" in payload


def test_decode_jwt_invalid_token():
    import jwt

    with pytest.raises(jwt.InvalidTokenError):
        decode_jwt("token_invalide")


def test_decode_jwt_tampered_token():
    import jwt

    token = create_jwt(1, "sam@mail.com")
    tampered = token + "xxx"

    with pytest.raises(jwt.InvalidTokenError):
        decode_jwt(tampered)


def test_save_and_get_token(tmp_path, monkeypatch):
    fake_file = tmp_path / ".epic_token"
    monkeypatch.setattr(
        "src.services.security.tokens.TOKEN_FILE",
        str(fake_file),
    )

    save_token("mon_token")
    result = get_token()

    assert result == "mon_token"
    assert fake_file.exists()


def test_get_token_missing(tmp_path, monkeypatch):
    fake_file = tmp_path / ".epic_token"
    monkeypatch.setattr(
        "src.services.security.tokens.TOKEN_FILE",
        str(fake_file),
    )

    result = get_token()

    assert result is None


def test_clear_token_success(tmp_path, monkeypatch):
    fake_file = tmp_path / ".epic_token"
    monkeypatch.setattr(
        "src.services.security.tokens.TOKEN_FILE",
        str(fake_file),
    )

    save_token("mon_token")
    result = clear_token()

    assert result is True
    assert not fake_file.exists()


def test_clear_token_missing(tmp_path, monkeypatch):
    fake_file = tmp_path / ".epic_token"
    monkeypatch.setattr(
        "src.services.security.tokens.TOKEN_FILE",
        str(fake_file),
    )

    result = clear_token()

    assert result is False

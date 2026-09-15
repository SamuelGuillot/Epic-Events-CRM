import pytest
from src.models import User, Department


def test_register_succes(auth_service, session):
    result = auth_service.register(
        full_name="Johnny Bravo",
        email="johnny@mail.com",
        password="motdepasse123",
        department="support",
    )

    assert result.success is True
    assert result.user is not None
    assert result.user.email == "johnny@mail.com"
    assert result.user.full_name == "Johnny Bravo"
    assert result.user.department == Department.SUPPORT
    assert result.token is not None


def test_register_email_deja_utilise(auth_service):
    auth_service.register(
        full_name="Johnny Bravo",
        email="johnny@mail.com",
        password="motdepasse123",
        department="support",
    )

    # Tentative avec le même email
    result = auth_service.register(
        full_name="Donnie Brasco",
        email="johnny@mail.com",
        password="autremotdepasse",
        department="commercial",
    )

    assert result.success is False
    assert "déjà utilisé" in result.message.lower()
    assert result.user is None


def test_register_departement_invalide(auth_service):
    result = auth_service.register(
        full_name="Johnny Bravo",
        email="johnny@mail.com",
        password="motdepasse123",
        department="informatique",
    )

    assert result.success is False
    assert "invalide" in result.message.lower()


def test_register_mot_de_passe_trop_court(auth_service):
    result = auth_service.register(
        full_name="Johnny Bravo",
        email="johnny@mail.com",
        password="court",
        department="support",
    )

    assert result.success is False
    assert "8 caractères" in result.message


def test_register_mot_de_passe_est_hache(auth_service, session):
    auth_service.register(
        full_name="Johnny Bravo",
        email="johnny@mail.com",
        password="motdepasse123",
        department="support",
    )

    user = session.query(User).filter(User.email == "johnny@mail.com").first()

    assert user is not None
    assert user.password_hash != "motdepasse123"
    assert user.password_hash.startswith("$argon2id$")


def test_register_numero_employe_auto(auth_service):
    result1 = auth_service.register(
        full_name="Johnny Bravo", email="johnny@mail.com",
        password="motdepasse123", department="support",
    )
    result2 = auth_service.register(
        full_name="Donnie Brasco", email="donnie@mail.com",
        password="motdepasse123", department="commercial",
    )

    assert result1.user.employee_number == "EMP001"
    assert result2.user.employee_number == "EMP002"



def test_login_succes(auth_service):
    auth_service.register(
        full_name="Johnny Bravo",
        email="johnny@mail.com",
        password="motdepasse123",
        department="support",
    )

    result = auth_service.login("johnny@mail.com", "motdepasse123")

    assert result.success is True
    assert result.user is not None
    assert result.user.email == "johnny@mail.com"
    assert result.token is not None


def test_login_email_inconnu(auth_service):
    result = auth_service.login("inconnu@mail.com", "motdepasse123")

    assert result.success is False
    assert "inconnu" in result.message.lower()
    assert result.user is None


def test_login_mauvais_mot_de_passe(auth_service):
    auth_service.register(
        full_name="Johnny Bravo",
        email="johnny@mail.com",
        password="motdepasse123",
        department="support",
    )

    result = auth_service.login("johnny@mail.com", "mauvais_mdp")

    assert result.success is False
    assert "incorrect" in result.message.lower()
    assert result.user is None

import typer

from src.exceptions import (
    NotAuthenticatedError,
    InvalidCredentialsError,
    EmailAlreadyUsedError,
    InvalidPasswordError,
    InvalidDepartmentError,
    UserNotFoundError,
    ClientNotFoundError,
    ContractNotFoundError,
    EventNotFoundError,
    ValidationError,
    ContractNotSignedError,
    EventAlreadyExistsError,
    PermissionDeniedError,
    EpicEventsError,
)


def _not_authenticated(e):
    return "vous n'etes pas connecte(e). Utilisez 'login'."

def _invalid_credentials(e):
    return "email ou mot de passe incorrect."

def _email_already_used(e):
    return f"l'email {e.email} est deja utilise."

def _invalid_password(e):
    return "le mot de passe doit contenir au moins 8 caracteres."

def _invalid_department(e):
    return (
        f"departement '{e.department}' invalide. "
        "Choisir : gestion, commercial, support."
    )

def _user_not_found(e):
    return f"utilisateur ID {e.user_id} introuvable."

def _client_not_found(e):
    return f"client ID {e.client_id} introuvable."

def _contract_not_found(e):
    return f"contrat ID {e.contract_id} introuvable."

def _event_not_found(e):
    return f"evenement ID {e.event_id} introuvable."

def _validation_error(e):
    return f"champ '{e.field}' invalide ({e.reason})."

def _contract_not_signed(e):
    return (
        f"le contrat #{e.contract_id} doit etre signe "
        "pour creer un evenement."
    )

def _event_already_exists(e):
    return (
        f"le contrat #{e.contract_id} a deja un evenement (ID {e.event_id})."
    )

def _permission_denied(e):
    return f"action '{e.action}' non autorisee."



HANDLERS = {
    NotAuthenticatedError: _not_authenticated,
    InvalidCredentialsError: _invalid_credentials,
    EmailAlreadyUsedError: _email_already_used,
    InvalidPasswordError: _invalid_password,
    InvalidDepartmentError: _invalid_department,
    UserNotFoundError: _user_not_found,
    ClientNotFoundError: _client_not_found,
    ContractNotFoundError: _contract_not_found,
    EventNotFoundError: _event_not_found,
    ValidationError: _validation_error,
    ContractNotSignedError: _contract_not_signed,
    EventAlreadyExistsError: _event_already_exists,
    PermissionDeniedError: _permission_denied,
}


def display_error(exception):
    """Traduit une exception en message utilisateur."""
    handler = HANDLERS.get(type(exception))

    if handler:
        typer.echo(f"Erreur : {handler(exception)}")
    elif isinstance(exception, EpicEventsError):
        typer.echo(f"Erreur : {exception}")
    else:
        typer.echo(f"Erreur inattendue : {exception}")
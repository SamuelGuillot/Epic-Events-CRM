import typer

from src.cli.app import app
from src.config.database import SessionLocal
from src.services.security.auth import AuthService
from src.services.security import clear_token, create_jwt
from src.DTO.user import RegisterData, LoginData, UserUpdateData
from src.exceptions import EpicEventsError
from src.permissions import can_update_user
from src.cli.decorators import has_permission
from src.cli.displays.auth_display import (
    display_user,
    display_register_result,
    display_login_result,
    display_logout_success,
    display_logout_not_connected,
)
from src.cli.displays.error_display import display_error


@app.command()
def register(
    full_name: str = typer.Option(..., prompt="Nom complet"),
    email: str = typer.Option(..., prompt="Email"),
    password: str = typer.Option(
        ..., prompt="Mot de passe", hide_input=True, confirmation_prompt=True
    ),
    department: str = typer.Option(..., prompt="Departement"),
):
    """Creer un nouveau compte collaborateur."""
    data = RegisterData(
        full_name=full_name,
        email=email,
        password=password,
        department=department,
    )

    with SessionLocal() as session:
        try:
            service = AuthService(session)
            user = service.register(data)
        except EpicEventsError as e:
            display_error(e)
            return

        token = create_jwt(user.id, user.email)
        display_register_result(user, token)


@app.command()
def login(
    email: str = typer.Option(..., prompt="Email"),
    password: str = typer.Option(..., prompt="Mot de passe", hide_input=True),
):
    """Se connecter au CRM."""
    data = LoginData(email=email, password=password)

    with SessionLocal() as session:
        try:
            service = AuthService(session)
            user = service.login(data)
        except EpicEventsError as e:
            display_error(e)
            return

        token = create_jwt(user.id, user.email)
        display_login_result(user, token)


@app.command()
def logout():
    """Se deconnecter (supprime le token stocke)."""
    if clear_token():
        display_logout_success()
    else:
        display_logout_not_connected()


@app.command("user-update")
@has_permission(can_update_user, "modifier un collaborateur")
def user_update(current_user, session, user_id: int = typer.Option(..., prompt="ID du collaborateur")):
    """Mettre a jour un collaborateur."""
    try:
        auth_service = AuthService(session)
        user = auth_service.get_user(user_id)

        name = typer.prompt("Nouveau nom (vide pour ne pas changer)", default="")
        email = typer.prompt("Nouvel email (vide pour ne pas changer)", default="")
        department = typer.prompt(
            "Nouveau departement (vide pour ne pas changer)", default=""
        )

        data = UserUpdateData(
            full_name=name or None,
            email=email or None,
            department=department or None,
        )

        user = auth_service.update_user(user_id, data)

    except EpicEventsError as e:
        display_error(e)
        return

    display_user(user)
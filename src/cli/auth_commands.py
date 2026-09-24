import typer

from src.cli.app import app
from src.config.database import SessionLocal
from src.services.auth import AuthService
from src.services.security import clear_token, create_jwt
from src.inputs.user import RegisterData, LoginData, UserUpdateData
from src.exceptions import EpicEventsError
from src.cli.display import display_user, display_error


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
            token = create_jwt(user.id, user.email)
            display_user(user)
            typer.echo(f"JWT : {token}")
        except EpicEventsError as e:
            display_error(e.message)


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
            token = create_jwt(user.id, user.email)
            typer.echo(f"Connexion reussie, bienvenue {user.full_name} !")
            typer.echo(f"JWT : {token}")
        except EpicEventsError as e:
            display_error(e.message)


@app.command()
def logout():
    """Se deconnecter (supprime le token stocke)."""
    if clear_token():
        typer.echo("Deconnexion reussie.")
    else:
        typer.echo("Vous n'etiez pas connecte(e).")


@app.command("user-update")
def user_update(
    user_id: int = typer.Option(..., prompt="ID du collaborateur"),
):
    """Mettre a jour un collaborateur."""
    with SessionLocal() as session:
        try:
            auth_service = AuthService(session)
            user = auth_service.get_user(user_id)

            name = typer.prompt("Nouveau nom (vide pour ne pas changer)", default="")
            email = typer.prompt("Nouvel email (vide pour ne pas changer)", default="")
            department = typer.prompt("Nouveau departement (vide pour ne pas changer)", default="")

            data = UserUpdateData(
                full_name=name or None,
                email=email or None,
                department=department or None,
            )

            user = auth_service.update_user(user_id, data)
            display_user(user)
        except EpicEventsError as e:
            display_error(e.message)
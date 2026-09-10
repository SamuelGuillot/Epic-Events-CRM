import typer
from src.config.database import SessionLocal
from src.services.auth import AuthService
from src.utils.security import clear_token

app = typer.Typer(help="Epic Events CRM")


@app.command()
def register(
    full_name: str = typer.Option(..., prompt="Nom complet"),
    email: str = typer.Option(..., prompt="Email"),
    password: str = typer.Option(
        ..., prompt="Mot de passe", hide_input=True, confirmation_prompt=True
    ),
    department: str = typer.Option(..., prompt="Departement"),
):
    with SessionLocal() as session:
        service = AuthService(session)
        result = service.register(full_name, email, password, department)

        if result.success:
            typer.echo(f"{result.message} !")
            typer.echo(f"Bienvenue {result.user.full_name} (ID: {result.user.id})")
            typer.echo(f"Matricule : {result.user.employee_number}")
            typer.echo(f"Departement : {result.user.department.value}")
            typer.echo(f"JWT : {result.token}")
        else:
            typer.echo(f"Erreur : {result.message}")


@app.command()
def login(
    email: str = typer.Option(..., prompt="Email"),
    password: str = typer.Option(..., prompt="Mot de passe", hide_input=True),
):
    """Se connecter au CRM."""
    with SessionLocal() as session:
        service = AuthService(session)
        result = service.login(email, password)

        if result.success:
            typer.echo(f"{result.message}, bienvenue {result.user.full_name} !")
            typer.echo(f"JWT : {result.token}")
        else:
            typer.echo(f"Erreur : {result.message}")

@app.command()
def logout():
    """Se deconnecter (supprime le token stocke)."""
    if clear_token():
        typer.echo("Deconnexion reussie.")
    else:
        typer.echo("Vous n'etiez pas connecte(e).")
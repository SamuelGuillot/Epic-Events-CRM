import typer


def display_user(user):
    typer.echo(f"ID : {user.id}")
    typer.echo(f"Nom : {user.full_name}")
    typer.echo(f"Email : {user.email}")
    typer.echo(f"Matricule : {user.employee_number}")
    typer.echo(f"Departement : {user.department.value}")


def display_register_result(user, token):
    typer.echo("Inscription reussie !")
    display_user(user)
    typer.echo(f"JWT : {token}")


def display_login_result(user, token):
    typer.echo(f"Connexion reussie, bienvenue {user.full_name} !")
    typer.echo(f"JWT : {token}")


def display_logout_success():
    typer.echo("Deconnexion reussie.")


def display_logout_not_connected():
    typer.echo("Vous n'etiez pas connecte(e).")


def display_error(message):
    typer.echo(f"Erreur : {message}")
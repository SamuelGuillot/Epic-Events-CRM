import typer


def display_clients(clients):
    if not clients:
        typer.echo("Aucun client trouve.")
        return

    typer.echo(f"{len(clients)} client(s) :")
    for client in clients:
        typer.echo("--------------------")
        display_client(client)


def display_client(client):
    typer.echo(f"  ID : {client.id}")
    typer.echo(f"  Nom : {client.full_name}")
    typer.echo(f"  Email : {client.email}")
    typer.echo(f"  Telephone : {client.phone or 'Non renseigne'}")
    typer.echo(f"  Societe : {client.company_name or 'Non renseigne'}")
    typer.echo(f"  Commercial : {client.commercial_name}")
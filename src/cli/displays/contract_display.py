import typer


def display_contracts(contracts):
    if not contracts:
        typer.echo("Aucun contrat trouve.")
        return

    typer.echo(f"{len(contracts)} contrat(s) :")
    for contract in contracts:
        typer.echo("--------------------")
        display_contract(contract)


def display_contract(contract):
    typer.echo(f"  ID : {contract.id}")
    typer.echo(f"  Client : {contract.client_name}")
    typer.echo(f"  Montant total : {contract.total_amount} €")
    typer.echo(f"  Reste a payer : {contract.remaining_amount} €")
    typer.echo(f"  Date de creation : {contract.creation_date}")
    statut = "Signe" if contract.status else "Non signe"
    typer.echo(f"  Statut : {statut}")

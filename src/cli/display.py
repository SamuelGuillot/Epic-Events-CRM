import typer


def display_register_result(result):
    if result.success:
        typer.echo(f"{result.message} !")
        typer.echo(f"Bienvenue {result.user.full_name} (ID: {result.user.id})")
        typer.echo(f"Matricule : {result.user.employee_number}")
        typer.echo(f"Departement : {result.user.department.value}")
        typer.echo(f"JWT : {result.token}")
    else:
        typer.echo(f"Erreur : {result.message}")


def display_login_result(result):
    if result.success:
        typer.echo(f"{result.message}, bienvenue {result.user.full_name} !")
        typer.echo(f"JWT : {result.token}")
    else:
        typer.echo(f"Erreur : {result.message}")

def display_clients(clients):
    if not clients:
        typer.echo("Aucun client trouve.")
        return

    typer.echo(f"{len(clients)} client(s) :")
    for client in clients:
        typer.echo("----------------------------")
        typer.echo(f"ID : {client.id}")
        typer.echo(f"Nom : {client.full_name}")
        typer.echo(f"Email : {client.email}")
        typer.echo(f"Telephone : {client.phone or 'Non renseigne'}")
        typer.echo(f"Societe : {client.company_name or 'Non renseigne'}")
        if client.commercial_contact:
            typer.echo(f"  Commercial : {client.commercial_contact.full_name}")
        else:
            typer.echo("  Commercial : Non assigne")


def display_client_result(result):
    if result.success:
        typer.echo(f"{result.message} !")
        typer.echo(f"ID: {result.client.id}")
        typer.echo(f"Nom: {result.client.full_name}")
        typer.echo(f"Email: {result.client.email}")
        typer.echo(f"Societe: {result.client.company_name or 'Non renseigne'}")
    else:
        typer.echo(f"Erreur: {result.message}")


def display_contracts(contracts):
    if not contracts:
        typer.echo("Aucun contrat trouve.")
        return

    typer.echo(f"{len(contracts)} contrat(s) :")
    for contract in contracts:
        typer.echo("--------------------")
        typer.echo(f"ID: {contract.id}")
        typer.echo(f"Client: {contract.client.full_name if contract.client else 'Inconnu'}")
        typer.echo(f"Montant total: {contract.total_amount} EUR")
        typer.echo(f"Reste a payer: {contract.remaining_amount} EUR")
        typer.echo(f"Date de creation: {contract.creation_date}")
        statut = "Signe" if contract.status else "Non signe"
        typer.echo(f"Statut: {statut}")


def display_contract_result(result):
    if result.success:
        typer.echo(f"{result.message} !")
        typer.echo(f"ID: {result.contract.id}")
        typer.echo(f"Client: {result.contract.client.full_name}")
        typer.echo(f"Montant total: {result.contract.total_amount} EUR")
        typer.echo(f"Reste a payer: {result.contract.remaining_amount} EUR")
        typer.echo(f"Date: {result.contract.creation_date}")
        statut = "Signe" if result.contract.status else "Non signe"
        typer.echo(f"Statut: {statut}")
    else:
        typer.echo(f"Erreur: {result.message}")
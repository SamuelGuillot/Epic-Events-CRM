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


def display_clients(clients):
    if not clients:
        typer.echo("Aucun client trouve.")
        return

    typer.echo(f"{len(clients)} client(s) :")
    for client in clients:
        typer.echo("--------------------")
        typer.echo(f"  ID : {client.id}")
        typer.echo(f"  Nom : {client.full_name}")
        typer.echo(f"  Email : {client.email}")
        typer.echo(f"  Telephone : {client.phone or 'Non renseigne'}")
        typer.echo(f"  Societe : {client.company_name or 'Non renseigne'}")
        if client.commercial_contact:
            typer.echo(f"  Commercial : {client.commercial_contact.full_name}")
        else:
            typer.echo("  Commercial : Non assigne")


def display_client(client):
    typer.echo(f"ID : {client.id}")
    typer.echo(f"Nom : {client.full_name}")
    typer.echo(f"Email : {client.email}")
    typer.echo(f"Telephone : {client.phone or 'Non renseigne'}")
    typer.echo(f"Societe : {client.company_name or 'Non renseigne'}")
    if client.commercial_contact:
        typer.echo(f"Commercial : {client.commercial_contact.full_name}")
    else:
        typer.echo("Commercial : Non assigne")


def display_contracts(contracts):
    if not contracts:
        typer.echo("Aucun contrat trouve.")
        return

    typer.echo(f"{len(contracts)} contrat(s) :")
    for contract in contracts:
        typer.echo("--------------------")
        typer.echo(f"  ID : {contract.id}")
        typer.echo(f"  Client : {contract.client.full_name if contract.client else 'Inconnu'}")
        typer.echo(f"  Montant total : {contract.total_amount} €")
        typer.echo(f"  Reste a payer : {contract.remaining_amount} €")
        typer.echo(f"  Date de creation : {contract.creation_date}")
        statut = "Signe" if contract.status else "Non signe"
        typer.echo(f"  Statut : {statut}")


def display_contract(contract):
    typer.echo(f"ID : {contract.id}")
    typer.echo(f"Client : {contract.client.full_name}")
    typer.echo(f"Montant total : {contract.total_amount} €")
    typer.echo(f"Reste a payer : {contract.remaining_amount} €")
    typer.echo(f"Date : {contract.creation_date}")
    statut = "Signe" if contract.status else "Non signe"
    typer.echo(f"Statut : {statut}")


def display_error(message):
    typer.echo(f"Erreur : {message}")

def display_events(events):
    if not events:
        typer.echo("Aucun evenement trouve.")
        return

    typer.echo(f"{len(events)} evenement(s) :")
    for event in events:
        typer.echo("-" * 40)
        display_event(event)


def display_event(event):
    typer.echo(f"  ID : {event.id}")
    typer.echo(f"  Nom : {event.event_name}")
    typer.echo(f"  Debut : {event.event_date_start}")
    typer.echo(f"  Fin : {event.event_date_end}")
    typer.echo(f"  Lieu : {event.location or 'Non renseigne'}")
    typer.echo(f"  Participants : {event.attendees_count}")
    if event.contract:
        typer.echo(f"  Contrat : #{event.contract.id}")
    if event.client:
        typer.echo(f"  Client : {event.client.full_name}")
    if event.support_contact:
        typer.echo(f"  Support : {event.support_contact.full_name}")
    else:
        typer.echo("  Support : Non assigne")
    if event.notes:
        typer.echo(f"  Notes : {event.notes}")
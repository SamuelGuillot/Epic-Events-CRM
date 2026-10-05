import typer


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
    typer.echo(f"  Contrat : #{event.contract_id}")
    typer.echo(f"  Client : {event.client_name}")
    typer.echo(f"  Support : {event.support_name}")
    if event.notes:
        typer.echo(f"  Notes : {event.notes}")

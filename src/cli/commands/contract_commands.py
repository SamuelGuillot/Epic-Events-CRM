import typer
from datetime import date

from src.cli.app import app
from src.cli.decorators import has_permission, has_object_permission
from src.config.database import SessionLocal
from src.services.client import ClientService
from src.services.contract import ContractService
from src.DTO.contract import ContractCreateData, ContractUpdateData
from src.permissions import can_create_contract, can_update_contract, can_sign_contract
from src.exceptions import EpicEventsError, PermissionDeniedError
from src.cli.displays.contract_display import display_contracts, display_contract
from src.cli.displays.error_display import display_error


def fetch_contract(session, contract_id, **kwargs):
    """Recupere un contrat par son ID (appele par le decorateur)."""
    service = ContractService(session)
    return service.get_contract(contract_id)


@app.command("contract-list")
def contract_list():
    """Afficher la liste de tous les contrats."""
    with SessionLocal() as session:
        try:
            service = ContractService(session)
            contracts = service.list_contracts()
        except EpicEventsError as e:
            display_error(e)
            return

        display_contracts(contracts)


@app.command("contract-create")
@has_permission(can_create_contract, "creer un contrat")
def contract_create(current_user, session):
    """Creer un nouveau contrat pour un client."""
    try:
        client_id = typer.prompt("ID du client", type=int)

        client_service = ClientService(session)
        client = client_service.get_client(client_id)

        total_amount = typer.prompt("Montant total", type=float)
        remaining_amount = typer.prompt("Montant restant a payer", type=float)

        data = ContractCreateData(
            client_id=client.id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            creation_date=date.today(),
        )

        contract_service = ContractService(session)
        contract = contract_service.create_contract(data, current_user)

    except EpicEventsError as e:
        display_error(e)
        return

    display_contract(contract)


@app.command("contract-update")
@has_object_permission(can_update_contract, fetch_contract, "modifier ce contrat")
def contract_update(
    current_user,
    session,
    object,
    contract_id: int = typer.Option(..., prompt="ID du contrat"),
    sign: bool = typer.Option(False, "--sign", help="Signer le contrat."),
):
    """Mettre a jour un contrat (montants, signature)."""
    if sign and not can_sign_contract(current_user):
        display_error(PermissionDeniedError("signer un contrat"))
        return

    try:
        total_amount = typer.prompt(
            "Nouveau montant total (vide pour ne pas changer)", default=""
        )
        remaining_amount = typer.prompt(
            "Nouveau montant restant (vide pour ne pas changer)", default=""
        )

        data = ContractUpdateData(
            total_amount=float(total_amount) if total_amount else None,
            remaining_amount=float(remaining_amount) if remaining_amount else None,
            status=True if sign else None,
        )

        contract_service = ContractService(session)
        contract = contract_service.update_contract(contract_id, data, current_user)

    except EpicEventsError as e:
        display_error(e)
        return

    display_contract(contract)
import typer
from datetime import date

from src.cli.app import app
from src.config.database import SessionLocal
from src.services.auth import AuthService
from src.services.client import ClientService
from src.services.contract import ContractService
from src.inputs.contract import ContractCreateData, ContractUpdateData
from src.exceptions import EpicEventsError
from src.cli.display import display_contracts, display_contract, display_error


@app.command("contract-list")
def contract_list():
    """Afficher la liste de tous les contrats."""
    with SessionLocal() as session:
        service = ContractService(session)
        contracts = service.list_contracts()
        display_contracts(contracts)


@app.command("contract-create")
def contract_create(
    client_id: int = typer.Option(..., prompt="ID du client"),
):
    """Creer un nouveau contrat pour un client."""
    with SessionLocal() as session:
        try:
            auth_service = AuthService(session)
            current_user = auth_service.get_current_user()

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
            display_contract(contract)
        except EpicEventsError as e:
            display_error(e.message)


@app.command("contract-update")
def contract_update(
    contract_id: int = typer.Option(..., prompt="ID du contrat"),
    sign: bool = typer.Option(False, "--sign", help="Signer le contrat."),
):
    """Mettre a jour un contrat (montants, signature)."""
    with SessionLocal() as session:
        try:
            contract_service = ContractService(session)
            contract = contract_service.get_contract(contract_id)

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

            contract = contract_service.update_contract(contract_id, data)
            display_contract(contract)
        except EpicEventsError as e:
            display_error(e.message)
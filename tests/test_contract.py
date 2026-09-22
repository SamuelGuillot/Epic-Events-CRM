from datetime import date
from src.services.contract import ContractService


def test_create_contract_succes(session, sam, make_client):
    client = make_client(sam)
    service = ContractService(session)

    result = service.create_contract(
        client_id=client.id,
        total_amount=5000.0,
        remaining_amount=5000.0,
        creation_date=date(2024, 1, 1),
        current_user=sam,
    )

    assert result.success is True
    assert result.contract is not None
    assert result.contract.total_amount == 5000.0
    assert result.contract.remaining_amount == 5000.0
    assert result.contract.status is False
    assert result.contract.client_id == client.id


def test_create_contract_client_introuvable(session, sam):
    service = ContractService(session)

    result = service.create_contract(
        client_id=9999,
        total_amount=5000.0,
        remaining_amount=5000.0,
        creation_date=date(2024, 1, 1),
        current_user=sam,
    )

    assert result.success is False
    assert result.contract is None
    assert "introuvable" in result.message.lower()


def test_create_contract_montant_total_negatif(session, sam, make_client):
    client = make_client(sam)
    service = ContractService(session)

    result = service.create_contract(
        client_id=client.id,
        total_amount=-100.0,
        remaining_amount=-100.0,
        creation_date=date(2024, 1, 1),
        current_user=sam,
    )

    assert result.success is False


def test_create_contract_montant_restant_negatif(session, sam, make_client):
    client = make_client(sam)
    service = ContractService(session)

    result = service.create_contract(
        client_id=client.id,
        total_amount=5000.0,
        remaining_amount=-500.0,
        creation_date=date(2024, 1, 1),
        current_user=sam,
    )

    assert result.success is False


def test_create_contract_restant_superieur_au_total(session, sam, make_client):
    client = make_client(sam)
    service = ContractService(session)

    result = service.create_contract(
        client_id=client.id,
        total_amount=1000.0,
        remaining_amount=5000.0,
        creation_date=date(2024, 1, 1),
        current_user=sam,
    )

    assert result.success is False
    assert "depasser" in result.message.lower()


def test_list_contracts_vide(session):
    service = ContractService(session)
    assert service.list_contracts() == []


def test_list_contracts_avec_donnees(session, sam, make_client):
    client = make_client(sam)
    service = ContractService(session)

    for i in range(3):
        service.create_contract(
            client_id=client.id,
            total_amount=1000.0,
            remaining_amount=1000.0,
            creation_date=date(2024, 1, 1),
            current_user=sam,
        )

    contracts = service.list_contracts()
    assert len(contracts) == 3
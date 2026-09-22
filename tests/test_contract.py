from datetime import date
import pytest
from src.services.contract import ContractService
from src.inputs.contract import ContractCreateData
from src.exceptions import ClientNotFoundError, ValidationError


def build_contract_data(client_id, **kwargs):
    defaults = {
        "client_id": client_id,
        "total_amount": 5000.0,
        "remaining_amount": 5000.0,
        "creation_date": date(2024, 1, 1),
    }
    defaults.update(kwargs)
    return ContractCreateData(**defaults)


def test_create_contract_success(session, sam, make_client):
    client = make_client(sam)
    service = ContractService(session)

    contract = service.create_contract(build_contract_data(client.id), sam)

    assert contract is not None
    assert contract.total_amount == 5000.0
    assert contract.remaining_amount == 5000.0
    assert contract.status is False
    assert contract.client_id == client.id


def test_create_contract_client_not_found(session, sam):
    service = ContractService(session)

    with pytest.raises(ClientNotFoundError):
        service.create_contract(build_contract_data(9999), sam)


def test_create_contract_negative_total(session, sam, make_client):
    client = make_client(sam)
    service = ContractService(session)

    with pytest.raises(ValidationError):
        service.create_contract(
            build_contract_data(client.id, total_amount=-100.0, remaining_amount=-100.0),
            sam,
        )


def test_create_contract_negative_remaining(session, sam, make_client):
    client = make_client(sam)
    service = ContractService(session)

    with pytest.raises(ValidationError):
        service.create_contract(
            build_contract_data(client.id, remaining_amount=-500.0),
            sam,
        )


def test_create_contract_remaining_above_total(session, sam, make_client):
    client = make_client(sam)
    service = ContractService(session)

    with pytest.raises(ValidationError):
        service.create_contract(
            build_contract_data(client.id, total_amount=1000.0, remaining_amount=5000.0),
            sam,
        )


def test_list_contracts_empty(session):
    service = ContractService(session)
    assert service.list_contracts() == []


def test_list_contracts_with_data(session, sam, make_client):
    client = make_client(sam)
    service = ContractService(session)

    for i in range(3):
        service.create_contract(build_contract_data(client.id), sam)

    contracts = service.list_contracts()
    assert len(contracts) == 3
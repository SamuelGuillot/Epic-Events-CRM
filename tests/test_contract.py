from datetime import date

import pytest

from src.DTO.contract import (
    ContractCreateData,
    ContractUpdateData,
)
from src.exceptions import (
    ClientNotFoundError,
    ContractNotFoundError,
    PermissionDeniedError,
    ValidationError,
)
from src.services.contract import ContractService


def build_contract_data(client_id, **kwargs):
    defaults = {
        "client_id": client_id,
        "total_amount": 5000.0,
        "remaining_amount": 5000.0,
        "creation_date": date(2024, 1, 1),
    }
    defaults.update(kwargs)
    return ContractCreateData(**defaults)


def test_create_contract_success(session, sam, dawn, make_client):
    client = make_client(sam)
    service = ContractService(session)

    contract = service.create_contract(
        build_contract_data(client.id), dawn
    )

    assert contract is not None
    assert contract.total_amount == 5000.0
    assert contract.remaining_amount == 5000.0
    assert contract.status is False
    assert contract.client_id == client.id


def test_create_contract_client_not_found(session, dawn):
    service = ContractService(session)

    with pytest.raises(ClientNotFoundError):
        service.create_contract(
            build_contract_data(9999), dawn
        )


def test_create_contract_remaining_above_total(
    session, sam, dawn, make_client
):
    client = make_client(sam)
    service = ContractService(session)

    with pytest.raises(ValidationError):
        service.create_contract(
            build_contract_data(
                client.id,
                total_amount=1000.0,
                remaining_amount=5000.0,
            ),
            dawn,
        )


def test_create_contract_permission_denied(
    session, sam, make_client
):
    """Un commercial ne peut pas creer de contrat."""
    client = make_client(sam)
    service = ContractService(session)

    with pytest.raises(PermissionDeniedError):
        service.create_contract(
            build_contract_data(client.id), sam
        )


def test_get_contract_success(
    session, sam, dawn, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client)
    service = ContractService(session)

    found = service.get_contract(contract.id)

    assert found is not None
    assert found.id == contract.id


def test_get_contract_not_found(session):
    service = ContractService(session)

    with pytest.raises(ContractNotFoundError):
        service.get_contract(867)


def test_list_contracts_empty(session):
    service = ContractService(session)

    assert service.list_contracts() == []


def test_list_contracts_with_data(
    session, sam, dawn, make_client
):
    client = make_client(sam)
    service = ContractService(session)

    for i in range(3):
        service.create_contract(
            build_contract_data(client.id), dawn
        )

    contracts = service.list_contracts()

    assert len(contracts) == 3



def test_list_by_client_empty(session, sam, make_client):
    client = make_client(sam)
    service = ContractService(session)

    assert service.list_by_client(client.id) == []


def test_list_by_client_with_data(
    session, sam, dawn, make_client
):
    client = make_client(sam)
    service = ContractService(session)

    for i in range(2):
        service.create_contract(
            build_contract_data(client.id), dawn
        )

    contracts = service.list_by_client(client.id)

    assert len(contracts) == 2


def test_update_contract_amounts(
    session, sam, dawn, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client)
    service = ContractService(session)

    data = ContractUpdateData(
        total_amount=3000.0,
        remaining_amount=1000.0,
    )
    updated = service.update_contract(contract.id, data, dawn)

    assert updated.total_amount == 3000.0
    assert updated.remaining_amount == 1000.0


def test_update_contract_sign(
    session, sam, dawn, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client, signed=False)
    service = ContractService(session)

    data = ContractUpdateData(status=True)
    updated = service.update_contract(contract.id, data, dawn)

    assert updated.status is True


def test_update_contract_sign_denied(
    session, sam, make_client, make_contract
):
    """Un commercial ne peut pas signer."""
    client = make_client(sam)
    contract = make_contract(client, signed=False)
    service = ContractService(session)

    data = ContractUpdateData(status=True)

    with pytest.raises(PermissionDeniedError):
        service.update_contract(contract.id, data, sam)


def test_update_contract_not_found(session, dawn):
    service = ContractService(session)
    data = ContractUpdateData(total_amount=1000.0)

    with pytest.raises(ContractNotFoundError):
        service.update_contract(1867, data, dawn)


def test_update_contract_negative_remaining(
    session, sam, dawn, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client)
    service = ContractService(session)

    data = ContractUpdateData(remaining_amount=-500.0)

    with pytest.raises(ValidationError):
        service.update_contract(contract.id, data, dawn)


def test_update_contract_remaining_above_total(
    session, sam, dawn, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client)
    service = ContractService(session)

    data = ContractUpdateData(
        total_amount=1000.0,
        remaining_amount=5000.0,
    )

    with pytest.raises(ValidationError):
        service.update_contract(contract.id, data, dawn)


def test_update_contract_permission_denied(
    session, sam, dawn, make_client, make_contract
):
    """Un commercial ne peut modifier que ses propres contrats."""
    client = make_client(dawn, name="Client Dawn", email="cd@mail.com")
    contract = make_contract(client)
    service = ContractService(session)

    data = ContractUpdateData(total_amount=1000.0)

    with pytest.raises(PermissionDeniedError):
        service.update_contract(contract.id, data, sam)

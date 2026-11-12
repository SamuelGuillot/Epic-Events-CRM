from src.permissions import (
    can_assign_support,
    can_create_client,
    can_create_contract,
    can_create_user,
    can_delete_user,
    can_filter_events_without_support,
    can_filter_own_events,
    can_filter_unpaid_contracts,
    can_filter_unsigned_contracts,
    can_sign_contract,
    can_update_client,
    can_update_contract,
    can_update_event,
    can_update_user,
)


def test_can_create_client_commercial(sam):
    assert can_create_client(sam) is True


def test_can_create_client_gestion(dawn):
    assert can_create_client(dawn) is False


def test_can_create_client_support(kate):
    assert can_create_client(kate) is False


def test_can_update_client_own(sam, make_client):
    client = make_client(sam)
    assert can_update_client(sam, client) is True


def test_can_update_client_other(sam, dawn, make_client):
    client = make_client(dawn)
    assert can_update_client(sam, client) is False


def test_can_update_client_gestion(dawn, sam, make_client):
    client = make_client(sam)
    assert can_update_client(dawn, client) is False


def test_can_update_client_support(kate, sam, make_client):
    client = make_client(sam)
    assert can_update_client(kate, client) is False


def test_can_create_contract_gestion(dawn):
    assert can_create_contract(dawn) is True


def test_can_create_contract_commercial(sam):
    assert can_create_contract(sam) is False


def test_can_create_contract_support(kate):
    assert can_create_contract(kate) is False


def test_can_update_contract_gestion(dawn, sam, make_client, make_contract):
    client = make_client(sam)
    contract = make_contract(client)
    assert can_update_contract(dawn, contract) is True


def test_can_update_contract_own_commercial(
    sam, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client)
    assert can_update_contract(sam, contract) is True


def test_can_update_contract_other_commercial(
    sam, dawn, make_client, make_contract
):
    client = make_client(dawn)
    contract = make_contract(client)
    assert can_update_contract(sam, contract) is False


def test_can_update_contract_support(
    kate, sam, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client)
    assert can_update_contract(kate, contract) is False


def test_can_sign_contract_gestion(dawn):
    assert can_sign_contract(dawn) is True


def test_can_sign_contract_commercial(sam):
    assert can_sign_contract(sam) is False


def test_can_sign_contract_support(kate):
    assert can_sign_contract(kate) is False


def test_can_filter_unsigned_contracts(sam, dawn, kate):
    assert can_filter_unsigned_contracts(sam) is True
    assert can_filter_unsigned_contracts(dawn) is True
    assert can_filter_unsigned_contracts(kate) is False


def test_can_filter_unpaid_contracts(sam, dawn, kate):
    assert can_filter_unpaid_contracts(sam) is True
    assert can_filter_unpaid_contracts(dawn) is True
    assert can_filter_unpaid_contracts(kate) is False


def test_can_update_event_gestion(
    dawn, sam, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client, signed=True)
    assert can_update_event(dawn, contract) is True


def test_can_update_event_support_own(
    kate, sam, make_client, make_contract, make_event
):
    client = make_client(sam)
    contract = make_contract(client, signed=True)
    event = make_event(contract, sam, support=kate)
    assert can_update_event(kate, event) is True


def test_can_update_event_support_other(
    kate, sam, make_client, make_contract, make_event
):
    client = make_client(sam)
    contract = make_contract(client, signed=True)
    event = make_event(contract, sam)  # sans support
    assert can_update_event(kate, event) is False


def test_can_update_event_commercial(
    sam, make_client, make_contract, make_event
):
    client = make_client(sam)
    contract = make_contract(client, signed=True)
    event = make_event(contract, sam)
    assert can_update_event(sam, event) is False


def test_can_assign_support_gestion(dawn):
    assert can_assign_support(dawn) is True


def test_can_assign_support_commercial(sam):
    assert can_assign_support(sam) is False


def test_can_assign_support_support(kate):
    assert can_assign_support(kate) is False


def test_can_filter_events_without_support(dawn, sam, kate):
    assert can_filter_events_without_support(dawn) is True
    assert can_filter_events_without_support(sam) is False
    assert can_filter_events_without_support(kate) is False


def test_can_filter_own_events(kate, sam, dawn):
    assert can_filter_own_events(kate) is True
    assert can_filter_own_events(sam) is False
    assert can_filter_own_events(dawn) is False


def test_can_create_user_gestion(dawn):
    assert can_create_user(dawn) is True


def test_can_create_user_commercial(sam):
    assert can_create_user(sam) is False


def test_can_create_user_support(kate):
    assert can_create_user(kate) is False


def test_can_update_user_gestion(dawn):
    assert can_update_user(dawn) is True


def test_can_update_user_commercial(sam):
    assert can_update_user(sam) is False


def test_can_delete_user_gestion(dawn):
    assert can_delete_user(dawn) is True


def test_can_delete_user_support(kate):
    assert can_delete_user(kate) is False

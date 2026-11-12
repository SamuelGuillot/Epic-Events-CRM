from datetime import datetime

import pytest

from src.DTO.event import EventCreateData, EventUpdateData
from src.exceptions import (
    ContractNotFoundError,
    ContractNotSignedError,
    EventAlreadyExistsError,
    EventNotFoundError,
    ValidationError,
)
from src.services.event import EventService


def build_event_data(contract_id, **kwargs):
    defaults = {
        "contract_id": contract_id,
        "event_name": "Test Event",
        "event_date_start": datetime(2026, 11, 15, 14, 0),
        "event_date_end": datetime(2026, 11, 15, 23, 0),
        "location": "Bordeaux",
        "attendees_count": 50,
        "notes": "Test notes",
    }
    defaults.update(kwargs)
    return EventCreateData(**defaults)


def test_create_event_success(
    session, sam, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client, signed=True)
    service = EventService(session)

    event = service.create_event(
        build_event_data(contract.id), sam
    )

    assert event is not None
    assert event.event_name == "Test Event"
    assert event.contract_id == contract.id
    assert event.attendees_count == 50


def test_create_event_contract_not_found(session, sam):
    service = EventService(session)

    with pytest.raises(ContractNotFoundError):
        service.create_event(build_event_data(9999), sam)


def test_create_event_contract_not_signed(
    session, sam, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client, signed=False)
    service = EventService(session)

    with pytest.raises(ContractNotSignedError):
        service.create_event(build_event_data(contract.id), sam)


def test_create_event_already_exists(
    session, sam, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client, signed=True)
    service = EventService(session)

    service.create_event(build_event_data(contract.id), sam)

    with pytest.raises(EventAlreadyExistsError):
        service.create_event(
            build_event_data(contract.id, event_name="Autre"),
            sam,
        )


def test_create_event_invalid_dates(
    session, sam, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client, signed=True)
    service = EventService(session)

    with pytest.raises(ValidationError):
        service.create_event(
            build_event_data(
                contract.id,
                event_date_start=datetime(2026, 11, 15, 23, 0),
                event_date_end=datetime(2026, 11, 15, 14, 0),
            ),
            sam,
        )


def test_get_event_success(
    session, sam, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client, signed=True)
    service = EventService(session)
    event = service.create_event(
        build_event_data(contract.id), sam
    )

    found = service.get_event(event.id)

    assert found is not None
    assert found.id == event.id


def test_get_event_not_found(session):
    service = EventService(session)

    with pytest.raises(EventNotFoundError):
        service.get_event(9999)


def test_get_event_by_contract(
    session, sam, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client, signed=True)
    service = EventService(session)
    service.create_event(build_event_data(contract.id), sam)

    found = service.get_event_by_contract(contract.id)

    assert found is not None
    assert found.contract_id == contract.id


def test_update_event_success(
    session, sam, dawn, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client, signed=True)
    service = EventService(session)
    event = service.create_event(
        build_event_data(contract.id), sam
    )

    data = EventUpdateData(event_name="Nouveau nom")
    updated = service.update_event(event.id, data, dawn)

    assert updated.event_name == "Nouveau nom"


def test_update_event_not_found(session, sam):
    service = EventService(session)
    data = EventUpdateData(event_name="Nouveau nom")

    with pytest.raises(EventNotFoundError):
        service.update_event(9999, data, sam)


def test_list_events_empty(session):
    service = EventService(session)

    assert service.list_events() == []


def test_list_events_with_data(
    session, sam, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client, signed=True)
    service = EventService(session)
    service.create_event(build_event_data(contract.id), sam)

    events = service.list_events()

    assert len(events) == 1


def test_list_events_without_support(
    session, sam, make_client, make_contract
):
    client = make_client(sam)
    contract = make_contract(client, signed=True)
    service = EventService(session)
    service.create_event(build_event_data(contract.id), sam)

    events = service.list_without_support()

    assert len(events) == 1
    assert events[0].support_name == "Non assigne"

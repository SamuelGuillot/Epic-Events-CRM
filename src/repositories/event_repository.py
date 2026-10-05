from src.DTO.event import EventRead
from src.models.event import Event


class EventRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        events = self.session.query(Event).order_by(Event.id).all()
        results = []
        for event in events:
            results.append(EventRead.from_model(event))
        return results

    def get_by_id(self, event_id):
        event = self.session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None
        return EventRead.from_model(event)

    def get_by_contract(self, contract_id):
        event = (
            self.session.query(Event)
            .filter(Event.contract_id == contract_id)
            .first()
        )
        if not event:
            return None
        return EventRead.from_model(event)

    def get_by_support(self, support_id):
        events = (
            self.session.query(Event)
            .filter(Event.support_contact_id == support_id)
            .order_by(Event.id)
            .all()
        )
        results = []
        for event in events:
            results.append(EventRead.from_model(event))
        return results

    def get_without_support(self):
        events = (
            self.session.query(Event)
            .filter(Event.support_contact_id.is_(None))
            .order_by(Event.id)
            .all()
        )
        results = []
        for event in events:
            results.append(EventRead.from_model(event))
        return results

    def add_event(self, data):
        event = Event(
            event_name=data.event_name,
            event_date_start=data.event_date_start,
            event_date_end=data.event_date_end,
            location=data.location,
            attendees_count=data.attendees_count or 0,
            notes=data.notes,
            contract_id=data.contract_id,
            client_id=data.client_id,
        )
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return EventRead.from_model(event)

    def update_event(self, event_id, data):
        event = self.session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None

        if data.event_name is not None:
            event.event_name = data.event_name
        if data.location is not None:
            event.location = data.location
        if data.attendees_count is not None:
            event.attendees_count = data.attendees_count
        if data.notes is not None:
            event.notes = data.notes
        if data.support_contact_id is not None:
            event.support_contact_id = data.support_contact_id

        self.session.commit()
        self.session.refresh(event)
        return EventRead.from_model(event)

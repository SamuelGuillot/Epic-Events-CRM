from src.models.event import Event


class EventRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Event).order_by(Event.id).all()

    def get_by_id(self, event_id):
        return self.session.query(Event).filter(Event.id == event_id).first()

    def get_by_contract(self, contract_id):
        return (
            self.session.query(Event)
            .filter(Event.contract_id == contract_id)
            .first()
        )

    def get_by_support(self, support_id):
        return (
            self.session.query(Event)
            .filter(Event.support_contact_id == support_id)
            .order_by(Event.id)
            .all()
        )

    def get_without_support(self):
        return (
            self.session.query(Event)
            .filter(Event.support_contact_id.is_(None))
            .order_by(Event.id)
            .all()
        )

    def add_event(self, data, client_id):
        event = Event(
            event_name=data.event_name,
            event_date_start=data.event_date_start,
            event_date_end=data.event_date_end,
            location=data.location,
            attendees_count=data.attendees_count or 0,
            notes=data.notes,
            contract_id=data.contract_id,
            client_id=client_id,
        )
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def update_event(self, event):
        self.session.commit()
        self.session.refresh(event)
        return event
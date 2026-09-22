from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.models.base import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(255), nullable=False)
    event_date_start = Column(DateTime, nullable=False)
    event_date_end = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=True)
    attendees_count = Column(Integer, nullable=False, default=0)
    notes = Column(Text, nullable=True)

    contract_id = Column(
        Integer,
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    client_id = Column(
        Integer,
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    support_contact_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    contract = relationship("Contract", back_populates="event")
    client = relationship("Client", back_populates="events")
    support_contact = relationship("User", back_populates="events_as_support")

    def __repr__(self):
        return f"<Event(id={self.id}, name={self.event_name})>"
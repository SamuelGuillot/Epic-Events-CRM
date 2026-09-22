from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.models.base import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    company_name = Column(String(255), nullable=True)
    first_contact_date = Column(Date, nullable=False)
    last_update_date = Column(Date, nullable=True)

    commercial_contact_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    commercial_contact = relationship("User", back_populates="clients")
    contracts = relationship("Contract", back_populates="client")
    events = relationship("Event", back_populates="client")

    def __repr__(self):
        return f"<Client(id={self.id}, full_name={self.full_name})>"
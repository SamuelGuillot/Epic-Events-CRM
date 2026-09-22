from sqlalchemy import Column, Integer, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.models.base import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)
    creation_date = Column(Date, nullable=False)
    status = Column(Boolean, nullable=False, default=False)

    client_id = Column(
        Integer,
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    commercial_contact_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    client = relationship("Client", back_populates="contracts")
    commercial_contact = relationship("User", back_populates="contracts_as_commercial")
    event = relationship("Event", back_populates="contract", uselist=False)

    def __repr__(self):
        return f"<Contract(id={self.id}, client_id={self.client_id}, total={self.total_amount})>"
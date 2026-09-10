from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
import enum
from src.models.base import Base
from sqlalchemy.orm import relationship


class Department(str, enum.Enum):
    GESTION = "gestion"
    COMMERCIAL = "commercial"
    SUPPORT = "support"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    employee_number = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    department = Column(Enum(Department), nullable=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    clients = relationship("Client", back_populates="commercial_contact")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
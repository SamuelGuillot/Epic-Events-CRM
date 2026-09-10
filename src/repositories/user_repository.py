"""
Couche Persistance (Repository) - Uniquement des requêtes SQL/ORM
"""
from sqlalchemy.orm import Session
from src.models.user import User

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()
    
    def save(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
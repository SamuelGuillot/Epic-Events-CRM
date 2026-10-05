from src.models.user import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    def get_by_email(self, email):
        """Retourne l'objet User (necessaire pour le login)."""
        return self.session.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id):
        """Retourne l'objet User (necessaire pour get_current_user)."""
        return self.session.query(User).filter(User.id == user_id).first()

    def add_user(self, user):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update_user(self, user):
        self.session.commit()
        self.session.refresh(user)
        return user

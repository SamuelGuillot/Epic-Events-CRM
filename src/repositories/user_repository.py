from src.models.user import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id):
        return self.session.query(User).filter(User.id == user_id).first()

    def add_user(self, user):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
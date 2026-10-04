from src.DTO.user import RegisterData, LoginData
from src.models.user import User, Department
from src.repositories.user_repository import UserRepository
from src.services.security.tokens import create_jwt, save_token, get_token, decode_jwt
from src.services.security.password import hash_password, verify_password
from src.exceptions import (
    InvalidCredentialsError,
    EmailAlreadyUsedError,
    NotAuthenticatedError,
    UserNotFoundError,
)


def generate_employee_number(compteur):
    return "EMP" + str(compteur).zfill(3)


class AuthService:
    def __init__(self, session):
        self.user_repo = UserRepository(session)

    def login(self, data: LoginData):
        data.validate()

        user = self.user_repo.get_by_email(data.email)
        if not user:
            raise InvalidCredentialsError()

        if not verify_password(data.password, user.password_hash):
            raise InvalidCredentialsError()

        token = create_jwt(user.id, user.email)
        save_token(token)
        return user


    def register(self, data: RegisterData):
        data.validate()

        if self.user_repo.get_by_email(data.email):
            raise EmailAlreadyUsedError(data.email)

        return self.create_user(data)

    def create_user(self, data: RegisterData):
        count = self.user_repo.session.query(User).count()
        employee_number = generate_employee_number(count + 1)
        dept = Department(data.department.lower())

        new_user = User(
            employee_number=employee_number,
            full_name=data.full_name,
            email=data.email,
            password_hash=hash_password(data.password),
            department=dept,
        )
        self.user_repo.add_user(new_user)
        return new_user

    def get_user(self, user_id):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"Utilisateur ID {user_id} introuvable.")
        return user

    def update_user(self, user_id, data):
        data.validate()
        user = self.get_user(user_id)

        if data.full_name is not None:
            user.full_name = data.full_name
        if data.email is not None:
            existing = self.user_repo.get_by_email(data.email)
            if existing and existing.id != user.id:
                raise EmailAlreadyUsedError("Cet email est deja utilise.")
            user.email = data.email
        if data.department is not None:
            user.department = Department(data.department.lower())

        return self.user_repo.update_user(user)

    def get_current_user(self):
        token = get_token()
        if not token:
            raise NotAuthenticatedError()

        try:
            payload = decode_jwt(token)
        except Exception:
            raise NotAuthenticatedError()

        user_id = payload.get("user_id")
        if not user_id:
            raise NotAuthenticatedError()

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotAuthenticatedError()

        return user
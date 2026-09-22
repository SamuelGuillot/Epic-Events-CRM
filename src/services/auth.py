from src.inputs.user import RegisterData, LoginData
from src.models.user import User, Department
from src.repositories.user_repository import UserRepository
from src.services.security import (
    create_jwt, hash_password, verify_password,
    save_token, get_token, decode_jwt
)
from src.exceptions import (
    InvalidCredentialsError,
    EmailAlreadyUsedError,
    NotAuthenticatedError,
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
            raise InvalidCredentialsError("Email inconnu.")

        if not verify_password(data.password, user.password_hash):
            raise InvalidCredentialsError("Mot de passe incorrect.")

        token = create_jwt(user.id, user.email)
        save_token(token)
        return user

    def register(self, data: RegisterData):
        data.validate()

        if self.user_repo.get_by_email(data.email):
            raise EmailAlreadyUsedError("Cet email est deja utilise.")

        new_user = self.create_user(data)
        return new_user

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

    def get_current_user(self):
        token = get_token()
        if not token:
            raise NotAuthenticatedError("Vous n'etes pas connecte(e).")

        try:
            payload = decode_jwt(token)
        except Exception:
            raise NotAuthenticatedError("Session invalide ou expiree.")

        user_id = payload.get("user_id")
        if not user_id:
            raise NotAuthenticatedError("Token invalide.")

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotAuthenticatedError("Utilisateur introuvable.")

        return user
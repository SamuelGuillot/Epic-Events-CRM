from dataclasses import dataclass
from src.models.user import User, Department
from src.repositories.user_repository import UserRepository
from src.services.security import (
    create_jwt, hash_password, verify_password,
    save_token, get_token, decode_jwt
)
from src.services.validators import is_valid_department, is_valid_password


def generate_employee_number(compteur):
    return "EMP" + str(compteur).zfill(3)


@dataclass
class RegisterResult:
    success: bool
    message: str
    user: User = None
    token: str = None


@dataclass
class LoginResult:
    success: bool
    message: str
    user: User = None
    token: str = None


class AuthService:
    def __init__(self, session):
        self.user_repo = UserRepository(session)

    def login(self, email, password):
        user = self.user_repo.get_by_email(email)
        if not user:
            return LoginResult(success=False, message="Email inconnu.")

        if not verify_password(password, user.password_hash):
            return LoginResult(success=False, message="Mot de passe incorrect.")

        token = create_jwt(user.id, user.email)
        save_token(token)

        return LoginResult(
            success=True,
            message="Connexion réussie",
            user=user,
            token=token,
        )

    def register(self, full_name, email, password, department):
        error = self.validate_registration(email, password, department)
        if error:
            return error

        new_user = self.create_user(full_name, email, password, department)
        token = create_jwt(new_user.id, new_user.email)

        return RegisterResult(
            success=True,
            message="Inscription réussie",
            user=new_user,
            token=token,
        )

    def validate_registration(self, email, password, department):
        if self.user_repo.get_by_email(email):
            return RegisterResult(success=False, message="Cet email est déjà utilisé.")

        if not is_valid_department(department):
            return RegisterResult(
                success=False,
                message="Département invalide. Choisir : gestion, commercial, support.",
            )

        if not is_valid_password(password):
            return RegisterResult(
                success=False,
                message="Le mot de passe doit contenir au moins 8 caractères.",
            )

        return None

    def create_user(self, full_name, email, password, department):
        count = self.user_repo.session.query(User).count()
        employee_number = generate_employee_number(count + 1)
        dept = Department(department.lower())

        new_user = User(
            employee_number=employee_number,
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            department=dept,
        )
        self.user_repo.save(new_user)
        return new_user

    def get_current_user(self):
        token = get_token()
        if not token:
            return None

        try:
            payload = decode_jwt(token)
            user_id = payload.get("user_id")
            if not user_id:
                return None
            return self.user_repo.get_by_id(user_id)
        except Exception as e:
            print(f"{e}")
            return None
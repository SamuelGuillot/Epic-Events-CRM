from dataclasses import dataclass
from src.models.user import User, Department
from src.repositories.user_repository import UserRepository
from src.utils.security import create_jwt, hash_password, verify_password, save_token


def generate_employee_number(compteur):
    """Génère un numéro d'employé au format EMP001, EMP002, etc."""
    return "EMP" + str(compteur).zfill(3)


@dataclass
class RegisterResult:
    """Résultat d'une tentative d'inscription."""
    success: bool
    message: str
    user: User = None
    token: str = None


@dataclass
class LoginResult:
    """Résultat d'une tentative de connexion."""
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
        return LoginResult(
            success=True,
            message="Connexion réussie",
            user=user,
            token=token
        )

    def register(self, full_name, email, password, department):
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            return RegisterResult(success=False, message="Cet email est déjà utilisé.")

        try:
            dept = Department(department.lower())
        except ValueError:
            return RegisterResult(
                success=False,
                message="Département invalide. Choisir : gestion, commercial, support."
            )


        if len(password) < 8:
            return RegisterResult(
                success=False,
                message="Le mot de passe doit contenir au moins 8 caractères."
            )

        count = self.user_repo.session.query(User).count()
        employee_number = generate_employee_number(count + 1)

        new_user = User(
            employee_number=employee_number,
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            department=dept
        )


        self.user_repo.save(new_user)

        token = create_jwt(new_user.id, new_user.email)
        save_token(token) 

        return RegisterResult(
            success=True,
            message="Inscription réussie",
            user=new_user,
            token=token
        )
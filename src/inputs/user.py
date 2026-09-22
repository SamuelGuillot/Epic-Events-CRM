from dataclasses import dataclass
from src.exceptions import ValidationError, InvalidDepartmentError, InvalidPasswordError
from src.models.user import Department


@dataclass
class RegisterData:
    full_name: str
    email: str
    password: str
    department: str

    def validate(self):
        if not self.full_name or not self.full_name.strip():
            raise ValidationError("Le nom complet est obligatoire.")

        if not self.email or "@" not in self.email or "." not in self.email:
            raise ValidationError("L'email est invalide.")

        if len(self.password) < 8:
            raise InvalidPasswordError(
                "Le mot de passe doit contenir au moins 8 caracteres."
            )

        try:
            Department(self.department.lower())
        except ValueError:
            raise InvalidDepartmentError(
                "Departement invalide. Choisir : gestion, commercial, support."
            )


@dataclass
class LoginData:
    email: str
    password: str

    def validate(self):
        if not self.email or "@" not in self.email:
            raise ValidationError("L'email est invalide.")

        if not self.password:
            raise ValidationError("Le mot de passe est obligatoire.")
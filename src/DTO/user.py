from dataclasses import dataclass

from src.exceptions import (
    InvalidDepartmentError,
    InvalidPasswordError,
    ValidationError,
)
from src.models.user import Department


@dataclass
class RegisterData:
    full_name: str
    email: str
    password: str
    department: str

    def validate(self):
        if not self.full_name or not self.full_name.strip():
            raise ValidationError("full_name", "obligatoire")
        if not self.email or "@" not in self.email or "." not in self.email:
            raise ValidationError("email", "format invalide")
        if len(self.password) < 8:
            raise InvalidPasswordError()
        try:
            Department(self.department.lower())
        except ValueError:
            raise InvalidDepartmentError(self.department)


@dataclass
class LoginData:
    email: str
    password: str

    def validate(self):
        if not self.email or "@" not in self.email:
            raise ValidationError("email", "format invalide")
        if not self.password:
            raise ValidationError("password", "obligatoire")


@dataclass
class UserUpdateData:
    full_name: str = None
    email: str = None
    department: str = None

    def validate(self):
        if self.full_name is not None and not self.full_name.strip():
            raise ValidationError("full_name", "ne peut pas etre vide")
        if self.email is not None and "@" not in self.email:
            raise ValidationError("email", "format invalide")
        if self.department is not None:
            try:
                Department(self.department.lower())
            except ValueError:
                raise InvalidDepartmentError(self.department)


@dataclass
class UserRead:
    id: int
    employee_number: str
    full_name: str
    email: str
    department: str

    @classmethod
    def from_model(cls, user):
        return cls(
            id=user.id,
            employee_number=user.employee_number,
            full_name=user.full_name,
            email=user.email,
            department=user.department.value,
        )

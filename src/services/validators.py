from src.models.user import Department


def is_valid_department(department):
    try:
        Department(department.lower())
        return True
    except ValueError:
        return False


def is_valid_password(password):
    return len(password) >= 8


def is_valid_email(email):
    if not email:
        return False
    return "@" in email and "." in email


def is_not_empty(value):
    return value is not None and value.strip() != ""
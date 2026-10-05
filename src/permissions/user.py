from src.models.user import Department


def can_create_user(user):
    return user.department == Department.GESTION


def can_update_user(user):
    return user.department == Department.GESTION


def can_delete_user(user):
    return user.department == Department.GESTION

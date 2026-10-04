from src.models.user import Department


def can_create_contract(user):
    return user.department == Department.GESTION


def can_update_contract(user, contract):
    if user.department == Department.GESTION:
        return True
    if user.department == Department.COMMERCIAL:
        return contract.commercial_contact_id == user.id
    return False


def can_sign_contract(user):
    return user.department == Department.GESTION


def can_filter_unsigned_contracts(user):
    return user.department in (Department.COMMERCIAL, Department.GESTION)


def can_filter_unpaid_contracts(user):
    return user.department in (Department.COMMERCIAL, Department.GESTION)
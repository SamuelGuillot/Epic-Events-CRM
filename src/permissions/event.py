from src.models.user import Department


def can_create_event(user, contract):
    return (
        user.department == Department.COMMERCIAL
        and contract.status is True
    )


def can_update_event(user, event):
    if user.department == Department.GESTION:
        return True
    if user.department == Department.SUPPORT:
        return event.support_contact_id == user.id
    return False


def can_assign_support(user):
    return user.department == Department.GESTION


def can_filter_events_without_support(user):
    return user.department == Department.GESTION


def can_filter_own_events(user):
    return user.department == Department.SUPPORT
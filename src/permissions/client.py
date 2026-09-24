from src.models.user import Department


def can_create_client(user):
    return user.department == Department.COMMERCIAL

def can_update_client(user, client):
    return (
        user.department == Department.COMMERCIAL
        and client.commercial_contact_id == user.id
    )
from functools import wraps
import makefun

from src.config.database import SessionLocal
from src.services.security.auth import AuthService
from src.exceptions import EpicEventsError, PermissionDeniedError
from src.cli.displays.error_display import display_error


def has_permission(permission, message):
    """Verifie une permission globale avant d'executer la commande."""
    def decorator(command):
        @makefun.wraps(command, remove_args=('current_user', 'session'))
        def wrapper(*args, **kwargs):
            with SessionLocal() as session:
                try:
                    auth_service = AuthService(session)
                    current_user = auth_service.get_current_user()

                    if not permission(current_user):
                        raise PermissionDeniedError(message)

                    return command(current_user, session, *args, **kwargs)
                except EpicEventsError as e:
                    display_error(e)
        return wrapper
    return decorator


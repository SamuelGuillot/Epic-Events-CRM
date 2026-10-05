from makefun import wraps

from src.cli.displays.error_display import display_error
from src.config.database import SessionLocal
from src.config.sentry import log_error
from src.exceptions import EpicEventsError, PermissionDeniedError
from src.services.security.auth import AuthService


def has_permission(permission, action):
    """Verifie une permission globale avant d'executer la commande."""
    def decorator(command):
        @wraps(command, remove_args=("current_user", "session"))
        def wrapper(*args, **kwargs):
            with SessionLocal() as session:
                try:
                    auth_service = AuthService(session)
                    current_user = auth_service.get_current_user()

                    if not permission(current_user):
                        raise PermissionDeniedError(action)

                    return command(current_user, session, *args, **kwargs)
                except EpicEventsError as e:
                    display_error(e)
                    return
                except Exception as e:
                    log_error(e)
                    display_error(e)
        return wrapper
    return decorator


def has_object_permission(permission, fetch, action):
    """Verifie une permission sur un objet avant d'executer la commande."""
    def decorator(command):
        @wraps(command, remove_args=("current_user", "session", "object"))
        def wrapper(*args, **kwargs):
            with SessionLocal() as session:
                try:
                    auth_service = AuthService(session)
                    current_user = auth_service.get_current_user()

                    obj = fetch(session, **kwargs)

                    if not permission(current_user, obj):
                        raise PermissionDeniedError(action)

                    return command(current_user, session, obj, *args, **kwargs)
                except EpicEventsError as e:
                    display_error(e)
                    return
                except Exception as e:
                    log_error(e)
                    display_error(e)
        return wrapper
    return decorator

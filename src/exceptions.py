class EpicEventsError(Exception):
    """Exception de base pour toutes les erreurs du CRM."""
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class InvalidCredentialsError(EpicEventsError):
    """Email ou mot de passe incorrect."""

class EmailAlreadyUsedError(EpicEventsError):
    """L'email est déjà pris par un autre utilisateur."""

class InvalidPasswordError(EpicEventsError):
    """Le mot de passe ne respecte pas les règles."""

class InvalidDepartmentError(EpicEventsError):
    """Le département n'existe pas."""

class UserNotFoundError(EpicEventsError):
    """Aucun utilisateur ne correspond à la recherche."""

class ClientNotFoundError(EpicEventsError):
    """Aucun client ne correspond à la recherche."""

class ContractNotFoundError(EpicEventsError):
    """Aucun contrat ne correspond à la recherche."""

class EventNotFoundError(EpicEventsError):
    """Aucun événement ne correspond à la recherche."""

class ValidationError(EpicEventsError):
    """Les données fournies ne sont pas valides."""

class PermissionDeniedError(EpicEventsError):
    """L'utilisateur n'a pas les droits pour cette action."""

class NotAuthenticatedError(EpicEventsError):
    """Aucun token valide n'est trouvé."""
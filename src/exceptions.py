class EpicEventsError(Exception):
    pass


class NotAuthenticatedError(EpicEventsError):
    pass


class InvalidCredentialsError(EpicEventsError):
    pass


class EmailAlreadyUsedError(EpicEventsError):
    def __init__(self, email):
        self.email = email


class InvalidPasswordError(EpicEventsError):
    pass


class InvalidDepartmentError(EpicEventsError):
    def __init__(self, department):
        self.department = department


class UserNotFoundError(EpicEventsError):
    def __init__(self, user_id):
        self.user_id = user_id


class ClientNotFoundError(EpicEventsError):
    def __init__(self, client_id):
        self.client_id = client_id


class ContractNotFoundError(EpicEventsError):
    def __init__(self, contract_id):
        self.contract_id = contract_id


class EventNotFoundError(EpicEventsError):
    def __init__(self, event_id):
        self.event_id = event_id


class ValidationError(EpicEventsError):
    def __init__(self, field, reason):
        self.field = field
        self.reason = reason


class ContractNotSignedError(EpicEventsError):
    def __init__(self, contract_id):
        self.contract_id = contract_id


class EventAlreadyExistsError(EpicEventsError):
    def __init__(self, contract_id, event_id):
        self.contract_id = contract_id
        self.event_id = event_id


class PermissionDeniedError(EpicEventsError):
    def __init__(self, action):
        self.action = action

class WindowManufacturingBotError(Exception):
    def __init__(self, message: str = "", custom_error_code: str = ""):
        super().__init__(message)
        self.custom_error_code = custom_error_code
        self.message = message


class DuplicateEntityError(WindowManufacturingBotError):
    def __init__(self, message: str = ""):
        super().__init__(message, custom_error_code="entity-duplicate")


class DuplicateUserError(DuplicateEntityError):
    def __init__(self, message: str = ""):
        super(DuplicateEntityError, self).__init__(
            message, custom_error_code="user-duplicate"
        )


class DuplicateChatError(DuplicateEntityError):
    def __init__(self, message: str = ""):
        super(DuplicateEntityError, self).__init__(
            message, custom_error_code="chat-duplicate"
        )


class EntityNotFoundError(WindowManufacturingBotError):
    def __init__(self, message: str = ""):
        super().__init__(message, custom_error_code="entity-notfound")


class UserNotFoundError(EntityNotFoundError):
    def __init__(self, message: str = ""):
        super(EntityNotFoundError, self).__init__(
            message, custom_error_code="user-notfound"
        )


class ChatNotFoundError(EntityNotFoundError):
    def __init__(self, message: str = ""):
        super(EntityNotFoundError, self).__init__(
            message, custom_error_code="chat-notfound"
        )


class UnauthorizeError(WindowManufacturingBotError):
    def __init__(self, message: str = ""):
        super().__init__(message, custom_error_code="unauthorized-error")
class AppException(Exception):
    """Base Exception for all our custom errors"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=404)

class ValidationException(AppException):
    def __init__(self, message: str = "Validation error occurred"):
        super().__init__(message=message, status_code=400)

class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message=message, status_code=401)

class ConflictException(AppException):
    def __init__(self, message: str = "Conflict"):
        super().__init__(message=message, status_code=409)

from app.shared.exceptions.exceptions import AppException

class AuthUserAlreadyExistsException(AppException):
    def __init__(self, email: str):
        super().__init__(
            message=f"A user with email {email} already exists.",
            status_code=400
        )

class InvalidCredentialsException(AppException):
    def __init__(self):
        super().__init__(
            message="Invalid email or password.",
            status_code=401
        )

class InvalidTokenException(AppException):
    def __init__(self, message: str = "Invalid or expired token."):
        super().__init__(
            message=message,
            status_code=401
        )

class UnauthorizedException(AppException):
    def __init__(self, message: str = "You do not have permission to perform this action."):
        super().__init__(
            message=message,
            status_code=403
        )

class AuthUserNotVerifiedException(AppException):
    def __init__(self, message: str = "User is not verified. Please verify your email via OTP."):
        super().__init__(
            message=message,
            status_code=403
        )

class InvalidOtpException(AppException):
    def __init__(self, message: str = "Invalid or expired OTP."):
        super().__init__(
            message=message,
            status_code=400
        )
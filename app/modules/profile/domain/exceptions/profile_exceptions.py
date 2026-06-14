from app.shared.exceptions.exceptions import AppException

class ProfileNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            message="Profile not found.",
            status_code=404
        )

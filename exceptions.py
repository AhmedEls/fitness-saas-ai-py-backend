class AppException(Exception):
    """Base exception for application-specific errors."""
    def __init__(self, message="An application error occurred", status_code=500):
 self.message = message
 self.status_code = status_code
 super().__init__(self.message)

class ProcessingError(AppException):
    """Exception raised for errors during data processing."""
    def __init__(self, message="Error during data processing", status_code=500):
 super().__init__(message, status_code)

class SuggestionGenerationError(AppException):
    """Exception raised for errors during suggestion generation."""
    def __init__(self, message="Error during suggestion generation", status_code=500):
 super().__init__(message, status_code)

class InvalidInputError(AppException):
    """Exception raised for invalid input data."""
    def __init__(self, message="Invalid input data", status_code=400):
        super().__init__(message, status_code)
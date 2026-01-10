"""Custom exceptions for Anymind SDK."""


class AnymindError(Exception):
    """Base exception for all Anymind errors."""
    pass


class ConfigurationError(AnymindError):
    """Raised when configuration is invalid or missing."""
    pass


class AuthenticationError(AnymindError):
    """Raised when authentication fails."""
    pass


class APIError(AnymindError):
    """Raised when API request fails."""
    
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class DeploymentError(AnymindError):
    """Raised when deployment fails."""
    pass


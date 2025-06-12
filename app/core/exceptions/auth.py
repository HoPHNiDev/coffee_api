from typing import Any, Dict, Optional

from core.exceptions.base import BaseAPIException


class AuthenticationError(BaseAPIException):
    """
    Base class for all authentication and authorization errors.

    This class sets HTTP status code 401 (Unauthorized) and provides
    a basic structure for all authentication-related exceptions.

    Attributes:
        detail (str): Detailed error message.
        error_type (str): Error type for client-side classification.
        extra (Optional[Dict[str, Any]]): Additional error data.
        status_code (int): HTTP status code (401 for authentication errors).
    """

    def __init__(
        self,
        detail: str = "Authentication error",
        error_type: str = "authentication_error",
        status_code: int = 401,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes AuthenticationError exception.

        Args:
            detail (str): Detailed error message.
            error_type (str): Error type for classification.
            extra (dict): Additional error data.
        """
        super().__init__(
            status_code=status_code,
            detail=detail,
            error_type=error_type,
            extra=extra or {},
        )


class InvalidCredentialsError(AuthenticationError):
    """
    Exception for invalid user credentials.

    Raised when a user provides an incorrect login or password
    during authentication.

    Attributes:
        detail (str): Fixed message "🔐 Invalid email or password".
        error_type (str): "invalid_credentials".
    """

    def __init__(self):
        """
        Initializes InvalidCredentialsError with predefined values.
        """
        super().__init__(
            detail="🔐 Invalid email or password",
            error_type="invalid_credentials",
        )


class TokenError(AuthenticationError):
    """
    Base class for all authentication token errors.

    Provides a common structure for errors occurring when working
    with JWT or other authentication tokens.

    Attributes:
        detail (str): Detailed error message.
        error_type (str): Error type for classification.
        extra (Optional[Dict[str, Any]]): Additional data with "token": True flag.
    """

    def __init__(
        self,
        detail: str,
        error_type: str = "token_error",
        status_code: int = 401,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes TokenError.

        Args:
            detail (str): Detailed error message.
            error_type (str): Error type for classification.
            extra (Optional[Dict[str, Any]]): Additional error data.
        """
        super().__init__(
            detail=detail,
            error_type=error_type,
            status_code=status_code,
            extra=extra or {"token": True},
        )


class TokenMissingError(TokenError):
    """
    Exception for missing token.

    Raised when a token is required for authentication but not provided
    in the request (e.g., missing Authorization header).

    Attributes:
        detail (str): "Token is missing".
        error_type (str): "token_missing".
    """

    def __init__(self):
        """
        Initializes TokenMissingError with predefined values.
        """
        super().__init__(detail="Token is missing", error_type="token_missing")


class TokenExpiredError(TokenError):
    """
    Exception for expired token.

    Raised when the provided authentication token is no longer valid
    due to expiration.

    Attributes:
        detail (str): "Token has expired".
        error_type (str): "token_expired".
    """

    def __init__(self):
        """
        Initializes TokenExpiredError with predefined values.
        """
        super().__init__(
            detail="Token has expired", error_type="token_expired", status_code=419
        )


class TokenInvalidError(TokenError):
    """
    Exception for invalid token.

    Raised when the provided token has an incorrect format,
    is corrupted, or the signature cannot be verified.
    """

    def __init__(
        self, detail: str = "Invalid token", extra: Optional[Dict[str, Any]] = None
    ):
        """
        Initializes TokenInvalidError.

        Args:
            detail: Error message
            extra: Additional error data
        """
        super().__init__(
            detail=detail, error_type="token_invalid", status_code=422, extra=extra
        )

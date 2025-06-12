"""
Exception classes for the users module.

This module contains exception classes
that may be raised when working with users.
"""

from typing import Any, Dict, Optional

from core.exceptions.base import BaseAPIException


class ForbiddenError(BaseAPIException):
    """
    Exception for forbidden access.

    Raised when the user does not have enough permissions to perform the operation.

    Attributes:
        detail (str): Detailed error message.
        required_role (Optional[str]): Required role to perform the operation.
        extra (Optional[Dict[str, Any]]): Additional error data.
    """

    def __init__(
        self,
        detail: str = "Insufficient permissions to perform the operation",
        required_role: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes ForbiddenError exception.

        Args:
            detail (str): Detailed error message.
            required_role (Optional[str]): Required role to perform the operation.
            extra_data (Optional[Dict[str, Any]]): Additional error data.
        """
        extra: Optional[Dict[str, Any]] = (
            {"required_role": required_role} if required_role else None
        )
        super().__init__(
            status_code=403, detail=detail, error_type="forbidden", extra=extra
        )


class AuthRequiredError(BaseAPIException):
    def __init__(
        self,
    ):
        super().__init__(
            status_code=403,
            detail="Authorization required.",
            error_type="auth_required",
        )


class SessionNotFoundError(BaseAPIException):
    def __init__(
        self,
        field: Optional[str] = None,
        value: Any = None,
        detail: Optional[str] = None,
    ):
        """
        Initializes SessionNotFoundError exception.

        Args:
            field (Optional[str]): Field used to search for the session.
            value (Any): Value of the field used to search for the session.
            detail (Optional[str]): Detailed error message.
        """
        message = detail or "Session not found"
        if field and value is not None:
            message = f"Session with {field}={value} not found"

        super().__init__(
            status_code=404,
            detail=message,
            error_type="session_not_found",
            extra={"field": field, "value": value} if field else None,
        )


class UserNotFoundError(BaseAPIException):
    """
    Exception for user not found.

    Raised when the requested user is not found in the database.

    Attributes:
        field (Optional[str]): Field used to search for the user.
        value (Any): Value of the field used to search for the user.
        detail (Optional[str]): Detailed error message.
    """

    def __init__(
        self,
        field: Optional[str] = None,
        value: Any = None,
        detail: Optional[str] = None,
    ):
        """
        Initializes UserNotFoundError exception.

        Args:
            field (Optional[str]): Field used to search for the user.
            value (Any): Value of the field used to search for the user.
            detail (Optional[str]): Detailed error message.
        """
        message = detail or "User not found"
        if field and value is not None:
            message = f"User with {field}={value} not found"

        super().__init__(
            status_code=404,
            detail=message,
            error_type="user_not_found",
            extra={"field": field, "value": value} if field else None,
        )


class UserExistsError(BaseAPIException):
    """
    Exception for existing user.

    Raised when trying to create a user with data that already exists in the system.

    Attributes:
        detail (str): Detailed error message.
        field (str): Field where the duplicate was found.
        value (Any): Value of the field that already exists.
    """

    def __init__(self, field: str, value: Any):
        """
        Initializes UserExistsError exception.

        Args:
            field (str): Field where the duplicate was found.
            value (Any): Value of the field that already exists.
        """
        super().__init__(
            status_code=409,
            detail=f"User with {field}={value} already exists",
            error_type="user_exists",
            extra={"field": field, "value": value},
        )

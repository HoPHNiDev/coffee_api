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
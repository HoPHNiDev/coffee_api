"""
Request schemas for authentication.

Contains Pydantic schemas for incoming data in authentication endpoints.
"""

from pydantic import EmailStr, Field, field_validator
from schemas.v1.base import BaseRequestSchema


class AuthSchema(BaseRequestSchema):
    """
    User authentication schema.

    Attributes:
        username (str): Username or email
        password: User password
        keep_alive (bool): Flag to keep the session alive (default is False)
    """

    username: str = Field(
        description="Username or email",
        examples=["user@example.com", "john_doe"],
    )
    password: str = Field(
        description="Password (minimum 8 characters, uppercase and lowercase letter, digit, special character)"
    )
    keep_alive: bool = Field(
        default=False,
        description="Flag to keep the session alive (default is False)",
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        """Username validation - can be email, phone, or regular name."""
        if "@" in v:
            return v
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")

        return v


class RegistrationRequestSchema(BaseRequestSchema):
    """
    Schema for registering a new user.

    Inherits from BaseRequestSchema and provides validation for all required
    fields to create a user account, including password strength and contact format checks.

    Attributes:
        username (str): Username (1 to 50 characters)
        email (EmailStr): User's email address (automatic format validation)
        password (str): Password with security requirements check

    Validation Rules:
        - username: Required, length from 1 to 50 characters
        - email: Required, valid email format
        - password: Required, checked by BasePasswordValidator
    """

    username: str = Field(
        min_length=1,
        max_length=50,
        description="Username (1 to 50 characters)",
        examples=["john_doe", "user123"],
    )

    email: EmailStr = Field(
        description="User's email address",
        examples=["user@example.com", "john.doe@company.org"],
    )

    password: str = Field(
        min_length=8,
        description=(
            "User password. Requirements: "
            "at least 8 characters, uppercase and lowercase letters, "
            "digit, special character"
        ),
        examples=["SecurePass123!", "MyP@ssw0rd"],
    )

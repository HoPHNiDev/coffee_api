"""
Response schemas for authentication errors.

Contains schemas for structured responses in case of authentication errors.
"""

from typing import Any, Dict

import pytz
from pydantic import Field

from schemas.v1.base import ErrorResponseSchema, ErrorSchema

moscow_tz = pytz.timezone("Europe/Moscow")

EXAMPLE_TIMESTAMP = "2025-01-01T00:00:00+03:00"
EXAMPLE_REQUEST_ID = "00000000-0000-0000-0000-000000000000"


class TokenExpiredErrorSchema(ErrorSchema):
    """Schema for expired token error. (419)"""

    detail: str = Field(default="Token has expired")
    error_type: str = Field(default="token_expired")
    status_code: int = Field(default=419)
    timestamp: str = Field(
        default=EXAMPLE_TIMESTAMP,
    )
    request_id: str = Field(default=EXAMPLE_REQUEST_ID)
    extra: Dict[str, Any] = Field(default={"token": True})


class TokenExpiredResponseSchema(ErrorResponseSchema):
    """Response schema for expired token error."""

    error: TokenExpiredErrorSchema


class TokenInvalidErrorSchema(ErrorSchema):
    """Schema for invalid token error. (422)"""

    detail: str = Field(default="Invalid token")
    error_type: str = Field(default="token_invalid")
    status_code: int = Field(default=422)
    timestamp: str = Field(
        default=EXAMPLE_TIMESTAMP,
    )
    request_id: str = Field(default=EXAMPLE_REQUEST_ID)
    extra: Dict[str, Any] = Field(default={"token": True})


class TokenInvalidResponseSchema(ErrorResponseSchema):
    """Response schema for invalid token error."""

    error: TokenInvalidErrorSchema


class TokenMissingErrorSchema(ErrorSchema):
    """Schema for missing token error. (401)"""

    detail: str = Field(default="Token is missing")
    error_type: str = Field(default="token_missing")
    status_code: int = Field(default=401)
    timestamp: str = Field(
        default=EXAMPLE_TIMESTAMP,
    )
    request_id: str = Field(default=EXAMPLE_REQUEST_ID)
    extra: Dict[str, Any] = Field(default={"token": True})


class TokenMissingResponseSchema(ErrorResponseSchema):
    """Response schema for missing token error."""

    error: TokenMissingErrorSchema

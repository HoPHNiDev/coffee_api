from typing import Optional

from .base import ErrorResponseSchema, ErrorSchema


class RateLimitErrorSchema(ErrorSchema):
    """
    Schema for representing rate limit exceeded error data.

    Attributes:
        detail: Detailed error description
        error_type: Error type (rate_limit_exceeded)
        status_code: HTTP response code (429)
        timestamp: Timestamp of the error occurrence
        request_id: Unique request identifier
        reset_time: Time in seconds until the limit resets
    """

    reset_time: Optional[int] = None


class RateLimitExceededResponseSchema(ErrorResponseSchema):
    """
    Response schema for rate limit exceeded errors.

    Attributes:
        success: Always False for errors
        message: Informational message, usually None for errors
        data: Always None for errors
        error: Detailed information about the rate limit exceeded error
    """

    error: RateLimitErrorSchema
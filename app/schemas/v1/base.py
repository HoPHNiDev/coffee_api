from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict
from fastapi import Query

class CommonBaseSchema(BaseModel):
    """
    Common base schema for all models.
    Contains only common configuration and the to_dict() method.

    Attributes:
        model_config (ConfigDict): Model configuration allowing
        the use of attributes as fields.

    Methods:
        to_dict(): Converts the object to a dictionary.
    """

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self) -> dict:
        return self.model_dump()

class BaseRequestSchema(CommonBaseSchema):
    """
    Base schema for input data.
    This class inherits from `CommonBaseSchema`
    and provides common configuration for all input schemas.

    There is no need to input id and creation/update dates for input data.
    """

    pass


class PaginationRequestSchema(BaseRequestSchema):
    """
    Schema for requests with offset and limit parameters.

    Attributes:
        offset (int): Offset for pagination.
        limit (int): Maximum number of items per page.
    """

    offset: int = Query(0, ge=0, description="Pagination offset")
    limit: int = Query(10, ge=1, description="Pagination limit")


class BaseCommonResponseSchema(CommonBaseSchema):
    """
    Base schema for API responses (without success and message).

    This class inherits from `CommonBaseSchema` and provides common
    configuration for all response schemas.
    """

    pass


class BaseResponseSchema(CommonBaseSchema):
    """
    Base schema for API responses.

    This class inherits from `CommonBaseSchema` and provides common
    configuration for all response schemas, including the ability to add
    metadata and error messages.

    Attributes:
        success (bool): Indicates whether the request was successful.
        message (Optional[str]): Message associated with the response.
    """

    success: bool = True
    message: Optional[str] = None


class ErrorSchema(CommonBaseSchema):
    """
    Schema for representing error data.

    Attributes:
        detail: Detailed error description
        error_type: Error type for client identification
        status_code: HTTP response code
        timestamp: Timestamp of the error occurrence
        request_id: Unique request identifier
        extra: Additional error data
    """

    detail: str
    error_type: str
    status_code: int
    timestamp: str
    request_id: str
    extra: Optional[Dict[str, Any]] = None


class ErrorResponseSchema(BaseResponseSchema):
    """
    Model for representing API errors in documentation.

    Matches the format of exceptions handled in handlers.py.
    Provides a unified error response format throughout the API.

    Attributes:
        success: Always False for errors
        message: Informational message, usually None for errors
        data: Always None for errors
        error: Detailed error information
    """

    success: bool = False
    message: Optional[str] = None
    data: None = None
    error: ErrorSchema

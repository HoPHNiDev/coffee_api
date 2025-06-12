"""
Response schemas for authentication.

Contains Pydantic schemas for outgoing data in authentication endpoints.
All schemas follow a unified format: {success, message, data}.
"""

from schemas.v1.base import BaseResponseSchema


class TokenResponseSchema(BaseResponseSchema):
    """
    Response schema with access token.

    Attributes:
        access_token: Main token for accessing protected resources.
        refresh_token: Token for obtaining a new access_token without re-authenticating the user.
        token_type: Type of token.
        expires_in: Token lifetime in seconds.
        message: Message about successful authentication.
    """

    access_token: None | str
    refresh_token: None | str
    token_type: str = "Bearer"
    expires_in: int
    message: str = "Authentication successful"
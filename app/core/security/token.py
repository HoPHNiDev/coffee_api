from datetime import datetime, timedelta
from typing import Any, Optional

from fastapi import Header
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from core.exceptions import (InvalidCredentialsError, TokenExpiredError,
                                 TokenInvalidError, TokenMissingError)
from core.config import settings
from loguru import logger

class TokenManager:
    """
    Class for working with JWT tokens.

    Provides static methods for generating, verifying, and validating tokens.
    Supports access, refresh, verification, and password reset tokens.
    """

    @staticmethod
    def access_valid_until() -> datetime:
        """
        Returns the expiration time of the access token in seconds.
        """
        return (
            datetime.now()
            + timedelta(minutes=settings.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    @staticmethod
    def refresh_valid_until() -> datetime:
        """
        Returns the expiration time of the refresh token in seconds.
        """
        return (
            datetime.now()
            + timedelta(days=settings.auth_jwt.REFRESH_TOKEN_EXPIRE_DAYS)
        )

    @staticmethod
    def generate_token(payload: dict) -> str:
        return jwt.encode(
            payload,
            key=settings.auth_jwt.PRIVATE_KEY.read_text(),
            algorithm=settings.auth_jwt.ALGORITHM,
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                key=settings.auth_jwt.PUBLIC_KEY.read_text(),
                algorithms=[settings.auth_jwt.ALGORITHM],
            )
        except ExpiredSignatureError as error:
            raise TokenExpiredError() from error
        except JWTError as error:
            raise TokenInvalidError() from error

    @staticmethod
    def verify_token(token: str) -> dict:
        if not token:
            raise TokenMissingError()
        return TokenManager.decode_token(token)

    @staticmethod
    def is_expired(expires_at: int) -> bool:
        current_timestamp = int(datetime.now().timestamp())
        return current_timestamp > expires_at

    @staticmethod
    def validate_token_payload(
        payload: dict, expected_type: Optional[str] = None
    ) -> dict:
        # Check token type (if specified)
        if expected_type:
            token_type = payload.get("type")
            if token_type != expected_type:
                logger.warning("Invalid token type")
                raise TokenInvalidError(f"Expected token type: {expected_type}")

        # Check expiration
        expires_at = payload.get("expires_at")
        if TokenManager.is_expired(expires_at):
            logger.warning("Token expired")
            raise TokenExpiredError()

        return payload

    @staticmethod
    def create_payload(session: Any) -> dict:
        return {
            "sub": session.id,
            "expires_at": int(session.valid_until.timestamp()),
            "type": "access",
        }

    @staticmethod
    def validate_payload(payload: dict) -> int:
        TokenManager.validate_token_payload(payload)

        session_id = payload.get("sub")
        if not session_id:
            raise InvalidCredentialsError()

        return session_id

    @staticmethod
    def create_refresh_payload(session: Any) -> dict:
        return {
            "sub": session.id,
            "expires_at": int(session.refreshable_until.timestamp()),
            "type": "refresh",
        }

    @staticmethod
    def validate_refresh_token(payload: dict) -> int:
        TokenManager.validate_token_payload(payload, "refresh")

        session_id = payload.get("sub")
        if not session_id:
            raise TokenInvalidError("Missed session_id in refresh token payload")

        return session_id


    @staticmethod
    def create_verification_payload(user_id: int) -> dict:
        return {
            "sub": str(user_id),
            "expires_at": int(
                (datetime.now() + timedelta(minutes=settings.auth_jwt.VERIFICATION_TOKEN_EXPIRE_MINUTES)).timestamp()
            ),
            "type": "verification",
        }

    @staticmethod
    def validate_verification_token(payload: dict) -> int:
        TokenManager.validate_token_payload(payload, "verification")

        user_id = payload.get("sub")
        if not user_id:
            raise TokenInvalidError("Missed user_id in verification token payload")

        return int(user_id)

    @staticmethod
    def get_token_from_header(
        authorization: str = Header(
            None, description="Header Authorization with token Bearer"
        ),
        optional: bool = True,
    ) -> str | None:
        if not authorization:
            if not optional:
                raise TokenMissingError()
            else:
                return None

        scheme, _, token = authorization.partition(" ")

        if scheme.lower() != "bearer":
            raise TokenInvalidError()

        if not token:
            raise TokenMissingError()

        return token

    @staticmethod
    def create_access_token(session_schema: Any) -> str:
        payload = TokenManager.create_payload(session_schema)

        logger.debug(
            f"Created access token for user ID: {session_schema.user_id}",
        )

        return TokenManager.generate_token(payload)

    @staticmethod
    def create_refresh_token(session_schema: Any) -> str:
        payload = TokenManager.create_refresh_payload(session_schema)

        logger.debug(f"Created refresh token for user ID: {session_schema.user_id}")

        return TokenManager.generate_token(payload)

    @staticmethod
    def create_verification_token(user_id: int) -> str:
        payload = TokenManager.create_verification_payload(user_id=user_id)

        logger.debug(f"Created verification token for user ID: {user_id}")

        return TokenManager.generate_token(payload)
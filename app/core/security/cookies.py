from fastapi import Response

from core.config import settings
from loguru import logger


class CookieManager:
    """
    Class for managing authentication cookies.

    Provides static methods for setting, reading, and deleting
    cookies with tokens. Uses security settings from the configuration.
    """

    ACCESS_TOKEN_KEY = "access_token"
    REFRESH_TOKEN_KEY = "refresh_token"

    @classmethod
    def set_auth_cookies(
        cls,
        response: Response,
        access_token: str,
        refresh_token: str
    ) -> None:
        """
        Sets cookies with authentication tokens.

        Sets both access and refresh tokens in separate cookies
        with appropriate security settings and lifetime.

        Args:
            response: HTTP response to set cookies
            access_token: Access token to set
            refresh_token: Refresh token to set
        """
        cls.set_access_token_cookie(response, access_token)
        cls.set_refresh_token_cookie(response, refresh_token)

        logger.debug(
            f"Authentication cookies set {len(access_token)=} {len(refresh_token)=}",
        )

    @classmethod
    def set_access_token_cookie(cls, response: Response, access_token: str) -> None:
        """
        Sets a cookie with the access token.

        Args:
            response: HTTP response to set the cookie
            access_token: Access token to set
        """
        response.set_cookie(
            key=cls.ACCESS_TOKEN_KEY,
            value=access_token,
            max_age=settings.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            domain=settings.COOKIE_DOMAIN,
            path="/",
        )

        logger.debug("Access token cookie set")

    @classmethod
    def set_refresh_token_cookie(cls, response: Response, refresh_token: str) -> None:
        """
        Sets a cookie with the refresh token.

        The refresh token is set only for the token refresh endpoint
        for additional security.

        Args:
            response: HTTP response to set the cookie
            refresh_token: Refresh token to set
        """
        response.set_cookie(
            key=cls.REFRESH_TOKEN_KEY,
            value=refresh_token,
            max_age=settings.auth_jwt.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            domain=settings.COOKIE_DOMAIN,
            path="/api/v1/auth/refresh",  # Only for refresh endpoint
        )

        logger.debug("Refresh token cookie set")

    @classmethod
    def clear_auth_cookies(cls, response: Response) -> None:
        cls.clear_access_token_cookie(response)
        cls.clear_refresh_token_cookie(response)

        logger.debug("Authentication cookies cleared")

    @classmethod
    def clear_access_token_cookie(cls, response: Response) -> None:
        response.delete_cookie(
            key=cls.ACCESS_TOKEN_KEY,
            path="/",
            domain=settings.COOKIE_DOMAIN,
        )

        logger.debug("Access token cookie cleared")

    @classmethod
    def clear_refresh_token_cookie(cls, response: Response) -> None:
        response.delete_cookie(
            key=cls.REFRESH_TOKEN_KEY,
            path="/api/v1/auth/refresh",
            domain=settings.COOKIE_DOMAIN,
        )

        logger.debug("Refresh token cookie cleared")
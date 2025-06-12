"""
Router for user authentication operations.

The module contains authentication routes, including logging in,
updating tokens, logging out, and password recovery. Provides
secure authentication using GWT tokens.

Routes:
    POST /auth/signup - User registration
    POST /auth/login - User authentication
    POST /auth/refresh - Refresh access token
    POST /auth/logout - Logout user

Classes:
    AuthRouter: Class for configuring authentication routes
"""

from fastapi import Header, Response, Cookie
from core.exceptions import TokenMissingError
from core.di import DUoW
from core.exceptions.user import AuthRequiredError
from core.security.token import TokenManager
from routes.base import BaseRouter
from schemas import (
    TokenExpiredResponseSchema,
    TokenInvalidResponseSchema,
    TokenMissingResponseSchema,
    TokenResponseSchema,
    RegistrationRequestSchema,
    BaseResponseSchema,
)
from core.security.cookies import CookieManager
from schemas.v1.auth.request import AuthSchema
from services.v1.auth.service import AuthService


class AuthRouter(BaseRouter):
    """
    Router for user authentication operations.
    """

    def __init__(self):
        super().__init__(prefix="auth", tags=["Authentication"])

    def configure(self):
        @self.router.post(
            path="/login",
            response_model=TokenResponseSchema,
            summary="User authentication",
            responses={
                200: {
                    "model": TokenResponseSchema,
                    "description": "Successful user authentication",
                },
            },
        )
        async def login(
            uow: DUoW,
            credentials: AuthSchema,
            response: Response,
            use_cookies: bool = True,
        ) -> TokenResponseSchema:
            """
            ## 🔐 User Authentication with Optional Cookie Usage

            Authenticates a user by username or email and returns JWT tokens.

            ### To authenticate, use one of the following:
            * **Email address**: user@example.com
            * **Username**: john_doe

            ### Parameters:
            * **username**: Email or username of the user
            * **password**: User's password
            * **use_cookies**: Boolean value indicating whether to use cookies for storing tokens (default is False)
            * **keep_alive**: Boolean value indicating whether to keep the session alive (default is False)

            ### Returns:
            * **success**: Boolean indicating authentication success
            * **message**: Message indicating successful authentication
            * **access_token**: JWT access token (valid for 15 minutes)
            * **refresh_token**: Refresh token (valid for 7 days)
            * **token_type**: Type of the token (Bearer)
            * **expires_in**: Access token lifetime in seconds
            """
            return await AuthService.login(
                response=response,
                uow=uow,
                credentials=credentials,
                use_cookies=use_cookies,
            )

        @self.router.post(
            path="/signup",
            response_model=BaseResponseSchema,
            summary="User Registration",
            responses={
                200: {
                    "model": BaseResponseSchema,
                    "description": "Successful user registration",
                },
            },
        )
        async def register(
            uow: DUoW, form_data: RegistrationRequestSchema
        ) -> BaseResponseSchema:
            """
            ## 🔐 Registration of a new user

            ### Parameters:
            * **username**: Username of new user
            * **email**: Email address of new user
            * **password**: Password for the new user (minimum 8 characters, must contain uppercase and lowercase letters, a digit, and a special character)

            ### Returns:
            * **success**: Boolean indicating successful registration
            * **message**: Message about successful registration
            """
            return await AuthService.register(
                uow=uow,
                form_data=form_data,
            )

        @self.router.post(
            path="/refresh",
            response_model=TokenResponseSchema,
            summary="Access Token Refresh",
            responses={
                200: {
                    "model": TokenResponseSchema,
                    "description": "Access token successfully refreshed",
                },
                401: {
                    "model": TokenMissingResponseSchema,
                    "description": "Refresh token is missing",
                },
                419: {
                    "model": TokenExpiredResponseSchema,
                    "description": "Refresh token has expired",
                },
                422: {
                    "model": TokenInvalidResponseSchema,
                    "description": "Invalid refresh token",
                },
            },
        )
        async def refresh_token(
            response: Response,
            uow: DUoW,
            refresh_token_header: str = Header(None, alias="refresh-token"),
            refresh_token_cookie: str = Cookie(
                None, alias=CookieManager.REFRESH_TOKEN_KEY
            ),
        ) -> TokenResponseSchema:
            """## 🔄 Access Token Refresh

            Obtain a new access token using a refresh token.
            Used when the access token has expired, but the refresh token is still valid.

            ### Headers:
            * **refresh_token_header**: Refresh token received during authentication
            * **refresh_token_cookie**: Refresh token from cookie (if cookies are used)

            ### Returns:
            * **success**: Boolean indicating whether the token was successfully refreshed
            * **message**: Message indicating successful token refresh
            * **data**: Updated token data
                * **access_token**: New JWT access token
                * **refresh_token**: New refresh token (token rotation)
                * **token_type**: Type of token (Bearer)
                * **expires_in**: Lifetime of the new access token in seconds

            ### Security:
            * Refresh tokens have a limited lifespan
            """
            token = refresh_token_header or refresh_token_cookie

            if not token:
                raise TokenMissingError()

            return await AuthService.refresh_token(
                response=response,
                uow=uow,
                refresh_token=token,
                use_cookies=bool(refresh_token_cookie),
            )

        @self.router.post(
            path="/logout",
            response_model=BaseResponseSchema,
            summary="Logout User",
            responses={
                200: {
                    "model": BaseResponseSchema,
                    "description": "Successful user logout",
                },
                401: {
                    "model": TokenMissingResponseSchema,
                    "description": "Access token is missing",
                },
                422: {
                    "model": TokenInvalidResponseSchema,
                    "description": "Access token is invalid",
                },
            },
        )
        async def logout(
            response: Response,
            uow: DUoW,
            refresh_token_header: str = Header(None, alias="access-token"),
            refresh_token_cookie: str = Cookie(
                None, alias=CookieManager.ACCESS_TOKEN_KEY
            ),
        ) -> BaseResponseSchema:
            """
            ## 🚪 Logout

            Ends the user's session and adds the tokens to a blacklist.
            After logout, all user tokens become invalid.

            ### Headers:
            * **access_token_header**: Access token received during authentication
            * **access_token_cookie**: Access token from cookie (if cookies are used)

            ### Returns:
            * **success**: Boolean indicating whether the logout was successful
            * **message**: Message confirming successful logout
            * **logged_out_at**: Timestamp of the logout

            ### Security:
            * All active user sessions are terminated
            * Re-authentication is required to regain access
            """
            token = TokenManager.get_token_from_header(
                refresh_token_header, optional=True
            )
            use_cookies = False
            if not token and refresh_token_cookie:
                token = refresh_token_cookie
                use_cookies = True
            else:
                raise AuthRequiredError()

            return await AuthService.logout(
                uow=uow,
                response=response,
                access_token=token,
                use_cookies=use_cookies,
            )
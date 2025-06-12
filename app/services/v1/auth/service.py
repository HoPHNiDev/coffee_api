from enum import Enum
from typing import Optional

from fastapi import Response
from loguru import logger

from core.exceptions import (
    InvalidPasswordError,
    TokenExpiredError,
    TokenInvalidError,

    ForbiddenError,
    SessionNotFoundError,
    UserNotFoundError,
    UserExistsError
)
from core.security.cookies import CookieManager
from core.security.token import TokenManager
from core.di import DUoW
from models import AuthSession
from schemas import (
    TokenResponseSchema,
    RegistrationRequestSchema,
    AuthSchema,
    BaseResponseSchema,

)
from schemas.v1.user.schemas import CurrentUserSchema
from services.v1.user.data_manager import UserDataManager
from services.v1.auth.data_manager import SessionDataManager



class TokenResponseAction(Enum):
    LOGIN = "auth"
    REFRESH = "refresh"


class AuthService:

    @classmethod
    async def register(
        cls,
        uow: DUoW,
        form_data: RegistrationRequestSchema,
    ) -> BaseResponseSchema:
        """
        Register a new user with the given credentials.
        """
        logger.info(f"Registering user {form_data.username}")

        field = "username"
        user = await UserDataManager.get_user(uow=uow, username=form_data.username)
        if not user:
            field = "email"
            user = await UserDataManager.get_user(uow=uow, email=form_data.email)

        if user:
            logger.warning(f"User {form_data.username} already exists")
            raise UserExistsError(field=field, value=getattr(form_data, field))

        user = await UserDataManager.create_user(uow=uow, form_data=form_data)

        logger.info(f"User {user.username} registered successfully")

        return BaseResponseSchema(
            message=f"User {user.username} registered successfully",
        )

    @classmethod
    async def login(
        cls,
        uow: DUoW,
        credentials: AuthSchema,
        response: Response,
        use_cookies: bool = True,
    ):
        """
        Login a user with the given credentials.
        """
        identifier = credentials.username
        logger.info(f"Logging in user {credentials.username}")

        user = await UserDataManager.get_user_by_identifier(
            uow=uow, identifier=identifier
        )

        if not user:
            logger.warning(f"User {identifier} not found")
            raise UserNotFoundError()

        if not user.is_active:
            logger.warning(f"User {identifier} disabled")
            raise ForbiddenError(
                detail="Account disabled",
                extra={"identifier": identifier},
            )

        if not user.verify_password(credentials.password):
            logger.warning(f"Invalid password for user {identifier}")
            raise InvalidPasswordError()

        user_schema = CurrentUserSchema.model_validate(user)
        session = await SessionDataManager.new_user_session(
            uow=uow,
            user=user_schema,
            keep_alive=credentials.keep_alive,
        )

        return await cls.return_token_response(
            session=session,
            response=response,
            use_cookies=use_cookies,
            action=TokenResponseAction.LOGIN,
        )

    @classmethod
    async def refresh_token(
        cls,
        uow: DUoW,
        refresh_token: str,
        response: Optional[Response] = None,
        use_cookies: bool = False,
    ) -> TokenResponseSchema:
        """
        Refresh access token using refresh token.
        """
        try:
            payload = TokenManager.decode_token(refresh_token)

            session_id = TokenManager.validate_refresh_token(payload)

            session = await SessionDataManager.get_session(
                uow=uow, extras=[uow.auth_session.model.user], id=session_id
            )

            if not session:
                logger.warning(
                    "Session not found or disabled",
                )
                raise SessionNotFoundError(field="id", value=session_id)

            if session.is_disabled:
                logger.warning("Session is disabled")
                raise SessionNotFoundError(field="id", value=session_id)

            if session.keep_alive:
                session.refreshable_until = TokenManager.refresh_valid_until()
            session.valid_until = TokenManager.access_valid_until()
            session = await SessionDataManager.update_session(uow=uow, data=session)

            return await cls.return_token_response(
                response=response,
                session=session,
                use_cookies=use_cookies,
                action=TokenResponseAction.REFRESH,
            )

        except (TokenExpiredError, TokenInvalidError) as e:
            logger.warning(
                f"Error while refreshing access token: {e}",
            )
            logger.exception(e)
            raise

    @classmethod
    async def logout(
        cls,
        uow: DUoW,
        access_token: str,
        response: Optional[Response] = None,
        use_cookies: bool = False,
    ) -> BaseResponseSchema:
        """
        Logout a user by invalidating the access token and optionally clearing cookies.
        """
        try:
            payload = TokenManager.decode_token(access_token)

            session_id = TokenManager.validate_payload(payload)

            session = await SessionDataManager.get_session(
                uow=uow, extras=[uow.auth_session.model.user], id=session_id
            )

            if session and not session.is_disabled:
                session.is_disabled = True
                await SessionDataManager.update_session(uow=uow, data=session)

        except (TokenExpiredError, TokenInvalidError) as e:
            logger.warning(
                f"Logout with invalid access token: {e}",
            )
            logger.exception(e)


        # Optionally cleaning cookies
        if response and use_cookies:
            CookieManager.clear_auth_cookies(response)

        return BaseResponseSchema(message="Logout successful")

    @classmethod
    async def return_token_response(
        cls,
        response: Response,
        session: AuthSession,
        use_cookies: bool,
        action: TokenResponseAction,
    ):
        access_token = await cls.create_token(session_schema=session)
        refresh_token = await cls.create_refresh_token(session_schema=session)

        logger.info(f"{action.value} successful")

        if response and use_cookies:
            CookieManager.set_auth_cookies(
                response=response,
                access_token=access_token,
                refresh_token=refresh_token,
            )
            return TokenResponseSchema(
                message=f"{action.value} successful",
                access_token=None,
                refresh_token=None,
                expires_in=int(session.valid_until.timestamp()),
            )
        return TokenResponseSchema(
            message=f"{action.value} successful",
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=int(session.valid_until.timestamp()),
        )

    @staticmethod
    async def create_token(session_schema: AuthSession) -> str:
        """
        Create JWT access token.

        Args:
            session_schema: User session.

        Returns:
            str: Access token
        """
        access_token = TokenManager.create_access_token(session_schema)

        logger.debug(f"Generated access token: {len(access_token)=}")

        return access_token

    @staticmethod
    async def create_refresh_token(session_schema: AuthSession) -> str:
        """
        Create JWT refresh token.

        Args:
            session_schema: User session.

        Returns:
            str: Refresh token
        """
        refresh_token = TokenManager.create_refresh_token(session_schema)

        logger.debug(
            f"Generated refresh token {len(refresh_token)=}",
        )

        return refresh_token

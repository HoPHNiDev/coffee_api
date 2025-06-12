from fastapi import Request, Cookie, Header

from loguru import logger
from core.exceptions import (
    TokenError,
    TokenInvalidError,
    TokenMissingError,
    AuthRequiredError,
    ForbiddenError
)
from core.di import DUoW
from core.security.cookies import CookieManager
from core.security.token import TokenManager
from models import User
from models.v1.user import UserRole
from schemas import CurrentUserSchema
from services.v1.auth.data_manager import SessionDataManager


class AuthenticationManager:
    @staticmethod
    async def get_current_user(
        request: Request,
        uow: DUoW,
        token_header: str = Header(None, alias="access-token"),
        token_cookie: str | None = Cookie(
            alias=CookieManager.ACCESS_TOKEN_KEY, default=None
        ),
    ) -> CurrentUserSchema | User:
        token = (
            TokenManager.get_token_from_header(token_header, optional=True)
            or token_cookie
        )
        logger.debug(
            f"Processing authentication request with headers: {request.headers}"
        )
        logger.debug(f"Starting to retrieve user data")
        logger.debug(f"Token received: {token}")

        if not token:
            logger.debug("Token is missing in the request")
            raise TokenMissingError()

        try:
            payload = TokenManager.verify_token(token)
            session_id = TokenManager.validate_payload(payload)
            session = await SessionDataManager.get_session(
                uow=uow, extras=[uow.auth_session.model.user], id=session_id
            )

            if not session:
                logger.debug(f"Session with ID {session_id} not found")
                raise AuthRequiredError()
            if session.is_disabled:
                logger.debug(f"Session with ID {session_id} is deactivated!")
                raise AuthRequiredError()
            if not session.user.is_active:
                logger.warning(f"User {session.user.id} disabled")
                raise ForbiddenError(
                    detail="Account disabled",
                    extra={"identifier": session.user.email or session.user.username},
                )

            logger.debug(f"User successfully authenticated: {session.user_id}")

            current_user = CurrentUserSchema.model_validate(session.user)

            return current_user

        except TokenError:
            raise
        except Exception as e:
            logger.debug("Error during authentication: %s", str(e))
            raise TokenInvalidError() from e


async def get_current_user(
    request: Request,
    uow: DUoW,
    token_header: str = Header(None, alias="access-token"),
    token_cookie: str | None = Cookie(
        alias=CookieManager.ACCESS_TOKEN_KEY, default=None
    ),
) -> CurrentUserSchema:
    return await AuthenticationManager.get_current_user(
        request=request, token_header=token_header, token_cookie=token_cookie, uow=uow
    )


async def get_current_user_optional(
    request: Request,
    uow: DUoW,
    token_header: str = Header(None, alias="access-token"),
    token_cookie: str | None = Cookie(
        alias=CookieManager.ACCESS_TOKEN_KEY, default=None
    ),
) -> CurrentUserSchema | None:
    try:
        return await AuthenticationManager.get_current_user(
            request=request,
            token_header=token_header,
            token_cookie=token_cookie,
            uow=uow,
        )
    except (TokenError, AuthRequiredError, ForbiddenError) as e:
        return None


async def admin_required(
    request: Request,
    uow: DUoW,
    token_header: str = Header(None, alias="access-token"),
    token_cookie: str | None = Cookie(
        alias=CookieManager.ACCESS_TOKEN_KEY, default=None
    ),
) -> CurrentUserSchema:
    user = await get_current_user(
        request=request, token_header=token_header, token_cookie=token_cookie, uow=uow
    )

    logger.debug(f"{user.role=}")
    if user.role != UserRole.ADMIN:
        raise ForbiddenError("You do not have permission to access this endpoint.")

    return user
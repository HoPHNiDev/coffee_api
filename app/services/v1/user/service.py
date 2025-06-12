from fastapi import Response
from loguru import logger
from core.di import DUoW
from core.exceptions import UserNotFoundError
from core.security.cookies import CookieManager
from schemas import (
    PaginationRequestSchema,
    BaseResponseSchema,
    UserSchema,
    CurrentUserSchema,
    UserUpdateRequestSchema,
)
from services.v1.user.data_manager import UserDataManager


class UserService:
    """
    User service for handling user-related operations.
    """

    @classmethod
    async def get_users(
        cls, uow: DUoW, pagination: PaginationRequestSchema
    ) -> list[UserSchema]:
        """
        Retrieve a paginated list of users.
        """

        users = await UserDataManager.get_users(
            uow, limit=pagination.limit, offset=pagination.offset
        )

        users_schema = [UserSchema.model_validate(user) for user in users]
        return users_schema

    @classmethod
    async def get_user(cls, uow: DUoW, user_id: int) -> UserSchema:
        """
        Retrieve a user by their ID.
        """
        user = await UserDataManager.get_user(uow=uow, id=user_id)
        if not user:
            raise UserNotFoundError()
        user_schema = UserSchema.model_validate(user)
        return user_schema

    @classmethod
    async def update_user(
        cls,
        form_data: UserUpdateRequestSchema,
        user_id: int,
        uow: DUoW,
    ) -> CurrentUserSchema | None:
        """
        Update user information by user ID.
        """
        user = await UserDataManager.get_user(uow=uow, id=user_id)

        if not user:
            raise UserNotFoundError()

        for key, value in form_data.model_dump().items():
            try:
                setattr(user, key, value)
            except AttributeError:
                logger.warning(f"Attempted to update non-existent field: {key}")

        updated_user = await UserDataManager.update(uow=uow, data=user)
        user_schema = CurrentUserSchema.model_validate(updated_user)

        return user_schema

    @classmethod
    async def delete_user(
        cls,
        uow: DUoW,
        user_id: int,
        response: Response,
    ) -> BaseResponseSchema:
        """
        Delete an active user by their ID.
        """

        user = await UserDataManager.get_user(uow=uow, id=user_id)
        if not user:
            raise UserNotFoundError()

        if user.is_active:
            user.is_active = False
            await UserDataManager.update(uow=uow, data=user)
        else:
            logger.warning(f"Attempted to delete non-active user: {user.username=}")

        if user.id == user_id:
            CookieManager.clear_auth_cookies(response)

        return BaseResponseSchema(message="Account has been deactivated")

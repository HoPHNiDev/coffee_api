from typing import Any

from sqlalchemy import Select

from core.security.token import TokenManager
from core.unitofwork import IUnitOfWork
from models import AuthSession
from schemas import CurrentUserSchema


class SessionDataManager:
    @classmethod
    async def get_session(
        cls,
        uow: IUnitOfWork,
        stmt: Select | None = None,
        fields: list[Any] | None = None,
        extras: list[Any] | None = None,
        **filters,
    ):
        session = await uow.auth_session.find_one(
            stmt=stmt, fields=fields, extras=extras, **filters
        )
        return session

    @classmethod
    async def get_sessions(
        cls,
        uow: IUnitOfWork,
        stmt: Select | None = None,
        fields: list[Any] | None = None,
        extras: list[Any] | None = None,
        **filters,
    ):
        sessions = await uow.auth_session.find_all(
            stmt=stmt, fields=fields, extras=extras, **filters
        )
        return sessions

    @classmethod
    async def create_session(cls, uow: IUnitOfWork, data):
        session = await uow.auth_session.add_one(data=data)
        await uow.session.commit()
        return session

    @classmethod
    async def update_session(cls, uow: IUnitOfWork, data):
        session = await uow.auth_session.edit_one(data=data)
        await uow.session.commit()
        return session

    @classmethod
    async def disable_user_sessions(cls, uow: IUnitOfWork, user_id: int):
        """
        Disable all sessions for a user.
        """
        sessions = await cls.get_sessions(uow=uow, user_id=user_id)
        for session in sessions:
            session.is_disabled = True
            await cls.update_session(uow=uow, data=session)
        return sessions

    @classmethod
    async def new_user_session(
        cls,
        uow: IUnitOfWork,
        user: CurrentUserSchema,
        keep_alive: bool = False,
    ):
        """
        Create a new session for a user.
        """
        await cls.disable_user_sessions(uow=uow, user_id=user.id)
        session = AuthSession(
            user_id=user.id,
            valid_until=TokenManager.access_valid_until(),
            refreshable_until=TokenManager.refresh_valid_until(),
            keep_alive=keep_alive,
        )
        await cls.create_session(uow=uow, data=session)
        return session

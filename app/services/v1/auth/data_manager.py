from typing import Any

from sqlalchemy import Select

from core.unitofwork import IUnitOfWork
from models import AuthSession


class SessionDataManager:
    @classmethod
    async def get_session(
        cls,
        uow: IUnitOfWork,
        stmt: Select | None = None,
        fields: list[Any] | None = None,
        extras: list[Any] | None = None,
        **filters,
    ) -> AuthSession | None:
        session = await uow.auth_session.find_one(
            stmt=stmt, fields=fields, extras=extras, **filters
        )
        return session

    @classmethod
    async def create_session(cls, uow: IUnitOfWork, data) -> AuthSession:
        session = await uow.auth_session.add_one(data=data)
        await uow.session.commit()
        return session

    @classmethod
    async def update_session(cls, uow: IUnitOfWork, data) -> AuthSession:
        session = await uow.auth_session.edit_one(data=data)
        await uow.session.commit()
        return session

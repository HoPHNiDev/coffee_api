from typing import Any

from sqlalchemy.sql.selectable import Select

from models import User
from core.unitofwork import IUnitOfWork


class UserDataManager:
    @classmethod
    async def get_user(
        cls,
        uow: IUnitOfWork,
        stmt: Select | None = None,
        fields: list[Any] | None = None,
        extras: list[Any] | None = None,
        **filters,
    ) -> User | None:
        user = await uow.user.find_one(
            stmt=stmt, fields=fields, extras=extras, **filters
        )
        return user

    @classmethod
    async def create(cls, uow: IUnitOfWork, data: User) -> User:
        user = await uow.user.add_one(data=data)
        await uow.session.commit()
        return user

    @classmethod
    async def update(cls, uow: IUnitOfWork, data: User) -> User:
        user = await uow.user.edit_one(data=data)
        await uow.session.commit()
        return user
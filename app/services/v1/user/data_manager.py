from typing import Any

from sqlalchemy import or_
from sqlalchemy.sql.selectable import Select

from models import User
from core.unitofwork import IUnitOfWork
from schemas.v1.auth.request import RegistrationRequestSchema


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
    async def get_users(cls, uow: IUnitOfWork, offset: int = 0, limit: int = 10):
        stmt = uow.user.select().order_by(uow.user.model.id).limit(limit).offset(offset)
        users = await uow.user.find_all(stmt=stmt)
        return users

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

    @classmethod
    async def get_user_by_identifier(
        cls, uow: IUnitOfWork, identifier: str
    ) -> User | None:
        """
        Retrieve a user by their identifier (username or email).
        """
        stmt = uow.user.select().where(
            or_(
                User.email == identifier,
                User.username == identifier,
            )
        )
        user = await uow.user.find_one(stmt=stmt)
        return user

    @classmethod
    async def create_user(
        cls, uow: IUnitOfWork, form_data: RegistrationRequestSchema
    ) -> User:
        """
        Create a new temp user by email.
        """
        user = User(email=form_data.email, username=form_data.username)
        user.set_password(form_data.password)
        return await cls.create(uow=uow, data=user)

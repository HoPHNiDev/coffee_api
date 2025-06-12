from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.selectable import Select
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from sqlmodel import SQLModel


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, data):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self):
        raise NotImplementedError

    @abstractmethod
    async def refresh(self, data):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: Any

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __find(
        self, stmt: Select | None = None, fields: list[Any] = None, extras: list[Any] | None = None, **filter_by
    ) -> Any:
        if stmt is not None:
            res = await self.execute_stmt(stmt)
            return res

        stmt = self.select(fields=fields)
        if filter_by:
            stmt = stmt.filter_by(**filter_by)
        if extras:
            for extra in extras:
                if isinstance(extra, list):
                    option = selectinload(extra[0])
                    for extra_extra in extra[1:]:
                        option = option.selectinload(extra_extra)
                    stmt = stmt.options(option)
                else:
                    stmt = stmt.options(selectinload(extra))
        res = await self.execute_stmt(stmt)
        return res

    async def add_one(self, data: SQLModel) -> Any:
        self.session.add(data)
        await self.session.commit()
        await self.refresh(data)
        return data

    async def edit_one(self, data: SQLModel) -> Any:
        self.session.add(data)
        await self.session.commit()
        await self.refresh(data)
        return data

    async def find_all(
        self,
        stmt: Select | None = None,
        fields: list[Any] | None = None,
        extras: list[Any] | None = None,
        **filter_by,
    ):
        res = await self.__find(stmt=stmt,fields=fields,  extras=extras, **filter_by)
        res = res.scalars().all()
        return res

    async def find_one(
        self,
        stmt: Select | None = None,
        fields: list[Any] | None = None,
        extras: list[Any] | None = None,
        **filter_by,
    ):
        res = await self.__find(stmt=stmt,fields=fields,  extras=extras, **filter_by)
        res = res.scalar_one_or_none()
        return res

    async def refresh(self, data: SQLModel, extras: list | None = None) -> Any:
        await self.session.refresh(data, attribute_names=extras)
        return data

    async def execute_stmt(self, stmt) -> Result:
        return await self.session.execute(stmt)

    def select(self, fields: list[Any] = None) -> Select:
        return select(*(fields or (self.model,)))

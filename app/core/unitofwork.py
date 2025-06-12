from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class IUnitOfWork(ABC):
    session: AsyncSession

    @abstractmethod
    def __init__(self):
        raise NotImplementedError


class UnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

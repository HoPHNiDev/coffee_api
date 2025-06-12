from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from repositories import UserRepository, AuthSessionRepository


class IUnitOfWork(ABC):
    session: AsyncSession
    user: UserRepository
    auth_session: AuthSessionRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError


class UnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user = UserRepository(self.session)
        self.auth_session = AuthSessionRepository(self.session)

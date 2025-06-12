from repositories.v1.base import SQLAlchemyRepository
from models import AuthSession

class AuthSessionRepository(SQLAlchemyRepository):
    model: AuthSession = AuthSession

    async def find_one(
        self,
        **kwargs
    ) -> AuthSession | None:
        return await super().find_one(**kwargs)

    async def find_all(
        self,
        **kwargs
    ) -> list[AuthSession]:
        return await super().find_all(**kwargs)

    async def add_one(self, data: AuthSession) -> AuthSession:
        return await super().add_one(data=data)

    async def edit_one(self, data: AuthSession) -> AuthSession:
        return await super().edit_one(data=data)

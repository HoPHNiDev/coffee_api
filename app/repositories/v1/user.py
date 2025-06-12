from repositories.v1.base import SQLAlchemyRepository
from models import User


class UserRepository(SQLAlchemyRepository):
    model: User = User

    async def find_one(
        self,
        **kwargs,
    ) -> User | None:
        return await super().find_one(**kwargs)

    async def find_all(
        self,
        **kwargs,
    ) -> list[User]:
        return await super().find_all(**kwargs)

    async def add_one(self, data: User) -> User:
        return await super().add_one(data=data)

    async def edit_one(self, data: User) -> User:
        return await super().edit_one(data=data)
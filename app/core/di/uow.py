from typing import AsyncGenerator, Annotated
from fastapi.params import Depends

from core.config import settings
from core.unitofwork import IUnitOfWork, UnitOfWork

async def get_uow() -> AsyncGenerator[IUnitOfWork, None]:
    async with settings.db_helper.session_factory() as session:
        uow = UnitOfWork(session)
        yield uow

DUoW = Annotated[UnitOfWork, Depends(get_uow)]
from typing import Annotated

from fastapi.params import Depends

from schemas.v1.user.schemas import CurrentUserSchema
from services.v1.auth.manager import (
    get_current_user,
    get_current_user_optional,
    admin_required,
)

DUser = Annotated[CurrentUserSchema, Depends(get_current_user)]
DUserAdmin = Annotated[CurrentUserSchema, Depends(admin_required)]
DUserOptional = Annotated[CurrentUserSchema | None, Depends(get_current_user_optional)]

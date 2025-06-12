from pydantic import Field, ConfigDict

from models.v1.user import UserRole, UserBase


class UserSchema(UserBase):
    id: int = Field(description="User ID")


class CurrentUserSchema(UserSchema):
    id: int = Field(description="User ID")
    role: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(description="Active status")
    is_verified: bool = Field(description="Verification status")

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self) -> dict:
        return self.model_dump()
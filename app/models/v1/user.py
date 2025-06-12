from typing import TYPE_CHECKING
from datetime import datetime

import bcrypt
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import LargeBinary, DateTime
from sqlmodel import Field, SQLModel, Column, Relationship
from enum import Enum

from models.v1.base import Base

if TYPE_CHECKING:
    from models import AuthSession

"""
In real projects I store Enums in separate files in enums/ directory,
but for simplicity I put them here.
"""
class UserRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


class UserBase(SQLModel):
    """
    User Base model.
    """

    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    # phone_number also could be added


class User(UserBase, Base, table=True):
    """
    User model.
    """

    password: bytes = Field(sa_column=Column(LargeBinary, nullable=False))
    role: UserRole = Field(default=UserRole.USER, nullable=False)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False, nullable=False)
    created_at: datetime | None = Field(sa_column=Column(DateTime, default=func.now()))
    updated_at: datetime | None = Field(
        sa_column=Column(DateTime, default=func.now(), onupdate=func.now())
    )

    sessions: list["AuthSession"] = Relationship(back_populates="user")
    @staticmethod
    def hash_password(password: str) -> bytes:
        """Generates a hashed version of the provided password."""
        pw = bytes(password, "utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pw, salt)

    def verify_password(self, password: str) -> bool:
        """Verify if provided password matches stored hash"""
        if not password or not self.password:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    def set_password(self, password: str) -> None:
        """Set a new password"""
        if not password:
            raise ValueError("Password cannot be empty")
        self.password = self.hash_password(password=password)

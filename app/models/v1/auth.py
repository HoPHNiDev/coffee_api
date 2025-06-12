from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, String, text, ForeignKey, DateTime, func
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models import User

class AuthSession(SQLModel, table=True):
    id: str = Field(
        sa_column=Column(
            String(10),
            primary_key=True,
            unique=True,
            nullable=False,
            default=text("substr(md5(random()::text), 1, 10)"),
        )
    )
    user_id: int | None = Field(
        sa_column=Column(ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    )
    user: Optional["User"] = Relationship(back_populates="sessions")

    is_disabled: bool = Field(default=False)

    keep_alive: bool = Field(default=False)
    valid_until: datetime | None = Field(sa_column=Column(DateTime))
    refreshable_until: datetime | None = Field(sa_column=Column(DateTime))

    created_at: datetime | None = Field(sa_column=Column(DateTime, default=func.now()))
    updated_at: datetime | None = Field(
        sa_column=Column(DateTime, default=func.now(), onupdate=func.now())
    )

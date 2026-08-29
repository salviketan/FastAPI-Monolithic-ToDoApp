from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from app.db.base_class import Base


# Mixin 1: Timestamps and Active state only
class TimestampMixin:
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


# Mixin 2: User Audit capability only
class UserAuditMixin:
    created_by_id: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_by_id: Mapped[int] = mapped_column(Integer, nullable=False)

    @declared_attr
    def __table_args__(cls) -> tuple[CheckConstraint, CheckConstraint]:
        return (
            CheckConstraint(
                "created_by_id > 0",
                name=f"check_{cls.__tablename__}_created_by_id_positive",
            ),
            CheckConstraint(
                "updated_by_id > 0",
                name=f"check_{cls.__tablename__}_updated_by_id_positive",
            ),
        )


class User(Base, TimestampMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(16), nullable=False)
    last_name: Mapped[str] = mapped_column(String(16), nullable=False)
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=True)
    # profile_img: Mapped[str | None] = mapped_column(
    #     String(256),
    #     nullable=True,
    #     default=None,
    # )

    task: Mapped[list["Task"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # @property
    # def image_path(self) -> str:
    #     if self.profile_img:
    #         return f"/media/profile_pics/{self.profile_img}"
    #     return "/static/profile_pics/default.jpg"


class Task(Base, TimestampMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(250), index=True, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )

    owner: Mapped["User"] = relationship(back_populates="task")

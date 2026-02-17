from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


class Task(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

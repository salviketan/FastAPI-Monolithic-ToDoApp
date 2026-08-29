from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select

from app.core.logger import debug_logger
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class.
        """
        self.model: type[ModelType] = model

    async def get(
        self,
        db: AsyncSession,
        idx: Any,
        options: list | None = None,
    ) -> ModelType | None:
        query: Select[tuple[ModelType]] = select(self.model).where(self.model.id == idx)

        if options:
            query = query.options(*options)

        result: Result[tuple[ModelType]] = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_kwargs(
        self,
        db: AsyncSession,
        kwargs: dict[str, Any],
        options: list | None = None,
    ) -> list[ModelType] | None:
        query: Select[tuple[ModelType]] = select(self.model).filter_by(**kwargs)

        if options:
            query = query.options(*options)

        result: Result[tuple[ModelType]] = await db.execute(query)
        return result.scalars().first()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        options: list | None = None,
    ) -> list[ModelType]:
        query: Select[tuple[ModelType]] = (
            select(self.model).offset(skip).limit(limit).order_by(self.model.id)
        )

        if options:
            query = query.options(*options)

        result: Result[tuple[ModelType]] = await db.execute(query)
        return result.scalars().all()

    async def create_from_dict(
        self,
        db: AsyncSession,
        *,
        obj_in_data: dict[str, Any],
    ) -> ModelType:

        debug_logger.debug("Creating %s", self.model.__name__)

        db_obj: ModelType = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        debug_logger.debug(
            "Successfully created %s [id=%s]",
            self.model.__name__,
            getattr(db_obj, "id", None),
        )

        return db_obj

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data: dict[str, Any] = jsonable_encoder(obj_in)
        db_obj: ModelType = await self.create_from_dict(db, obj_in_data=obj_in_data)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
        refresh_attributes: list[str] | None = None,
    ) -> ModelType:
        obj_id: Any | None = getattr(db_obj, "id", None)
        if isinstance(obj_in, dict):
            update_data: dict[str, Any] = obj_in
        else:
            update_data: dict[str, Any] = obj_in.model_dump(exclude_unset=True)

        debug_logger.debug("Updating %s [id=%s]", self.model.__name__, obj_id)

        obj_data: dict[str, Any] = jsonable_encoder(db_obj)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()

        if refresh_attributes:
            await db.refresh(db_obj, attribute_names=refresh_attributes)
        else:
            await db.refresh(db_obj)

        debug_logger.debug(
            "Successfully updated %s [id=%s]",
            self.model.__name__,
            obj_id,
        )

        return db_obj

    async def remove(self, db: AsyncSession, *, idx: int) -> ModelType:
        debug_logger.debug("Attempting to delete %s [id=%s]", self.model.__name__, idx)

        query: Select[tuple[ModelType]] = select(self.model).where(self.model.id == idx)
        result: Result[tuple[ModelType]] = await db.execute(query)
        obj: ModelType | None = result.scalar_one_or_none()
        if obj:
            await db.delete(obj)
            await db.commit()
            debug_logger.debug(
                "Successfully deleted %s [id=%s]",
                self.model.__name__,
                idx,
            )
        else:
            debug_logger.debug(
                "Delete failed: %s [id=%s] not found",
                self.model.__name__,
                idx,
            )
        return obj

from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select

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

    def get(
        self,
        db: Session,
        idx: Any,
        options: list | None = None,
    ) -> ModelType | None:
        query: Select[tuple[ModelType]] = select(self.model).where(self.model.id == idx)

        if options:
            query = query.options(*options)

        return db.execute(query).scalar_one_or_none()

    def get_by_kwargs(
        self,
        db: Session,
        kwargs: dict[str, Any],
        options: list | None = None,
    ) -> list[ModelType] | None:
        query: Select[tuple[ModelType]] = select(self.model).filter_by(**kwargs)

        if options:
            query = query.options(*options)

        return db.execute(query).scalars().first()

    def get_multi(
        self,
        db: Session,
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

        return db.execute(query).scalars().all()

    def create_from_dict(
        self,
        db: Session,
        *,
        obj_in_data: dict[str, Any],
    ) -> ModelType:
        db_obj: ModelType = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data: dict[str, Any] = jsonable_encoder(obj_in)
        db_obj: ModelType = self.create_from_dict(db, obj_in_data=obj_in_data)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
        refresh_attributes: list[str] | None = None,
    ) -> ModelType:
        obj_data: dict[str, Any] = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data: dict[str, Any] = obj_in
        else:
            update_data: dict[str, Any] = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()

        if refresh_attributes:
            db.refresh(db_obj, attribute_names=refresh_attributes)
        else:
            db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, idx: int) -> ModelType:
        query: Select[tuple[ModelType]] = select(self.model).where(self.model.id == idx)
        obj: ModelType | None = db.execute(query).scalar_one_or_none()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

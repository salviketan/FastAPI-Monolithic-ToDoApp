from typing import Annotated, Any

import crud
import models
import schemas
from api import deps
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "",
    response_model=list[schemas.Task],
)
def get_tasks(
    db: Annotated[Session, Depends(deps.get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[models.Task]:
    tasks: list[models.Task] = crud.task.get_multi(
        db,
        skip=skip,
        limit=limit,
    )

    return tasks


@router.post(
    "",
    response_model=schemas.Task,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    *,
    task_in: schemas.TaskCreate,
    db: Annotated[Session, Depends(deps.get_db)],
) -> Any:
    task_in_data: dict[str, Any] = jsonable_encoder(task_in)
    task: list[models.Task] | None = crud.task.get_by_kwargs(
        db=db,
        kwargs={"name": task_in_data["name"]},
    )
    if task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task already exists.",
        )
    task = crud.task.create(db, obj_in=task_in)
    return task


@router.get(
    "/{id}",
    response_model=schemas.Task,
    status_code=status.HTTP_200_OK,
)
def get_task(
    *,
    id: int,  # noqa: A002
    db: Annotated[Session, Depends(deps.get_db)],
) -> Any:
    task: models.Task | None = crud.task.get(db, id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task doesn't exists.",
        )
    return task

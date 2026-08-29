from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get(
    "",
    response_model=list[schemas.Task],
)
async def get_tasks(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[models.Task]:
    tasks: list[models.Task] = await crud.task.get_multi(
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
async def create_task(
    *,
    task_in: schemas.TaskCreate,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
) -> Any:
    task_in_data: dict[str, Any] = jsonable_encoder(task_in)

    user: models.User | None = await crud.user.get(db=db, idx=task_in_data["owner_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exists.",
        )

    task: list[models.Task] | None = await crud.task.get_by_kwargs(
        db=db,
        kwargs={"name": task_in_data["name"]},
    )
    if task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task already exists.",
        )
    task = await crud.task.create(db, obj_in=task_in)
    return task


@router.get(
    "/{id}",
    response_model=schemas.Task,
    status_code=status.HTTP_200_OK,
)
async def get_task(
    *,
    id: int,  # noqa: A002
    db: Annotated[AsyncSession, Depends(deps.get_db)],
) -> Any:
    task: models.Task | None = await crud.task.get(db=db, idx=id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task doesn't exists.",
        )
    return task


@router.patch(
    "/{id}",
    response_model=schemas.Task,
    status_code=status.HTTP_200_OK,
)
async def update_task(
    *,
    id: int,  # noqa: A002
    task_in: schemas.TaskUpdate,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
) -> Any:
    task: models.Task | None = await crud.task.get(db=db, idx=id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task doesn't exists.",
        )
    task = await crud.task.update(db=db, db_obj=task, obj_in=task_in)

    return task


@router.delete(
    "/{id}",
    response_model=schemas.Task,
    status_code=status.HTTP_200_OK,
)
async def delete_task(
    *,
    id: int,  # noqa: A002
    db: Annotated[AsyncSession, Depends(deps.get_db)],
) -> Any:
    task: models.Task | None = await crud.task.get(db=db, idx=id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task doesn't exists.",
        )
    task = await crud.task.remove(db=db, idx=id)

    return task

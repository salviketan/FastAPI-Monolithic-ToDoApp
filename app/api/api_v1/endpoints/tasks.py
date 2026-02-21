from typing import Annotated

import crud
import models
import schemas
from api import deps
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("", response_model=list[schemas.Task])
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

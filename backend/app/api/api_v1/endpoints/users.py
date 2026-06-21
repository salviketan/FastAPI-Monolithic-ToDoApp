from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get(
    "",
    response_model=list[schemas.User],
)
def get_users(
    db: Annotated[Session, Depends(deps.get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[models.Users]:
    users: list[models.Users] = crud.user.get_multi(
        db,
        skip=skip,
        limit=limit,
    )

    return users


@router.get(
    "/{id}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
)
def get_user(
    id: int,  # noqa: A002
    db: Annotated[Session, Depends(deps.get_db)],
) -> Any:
    user: models.Users | None = crud.user.get(db, idx=id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exists.",
        )

    return user

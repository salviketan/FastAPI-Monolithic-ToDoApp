from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get(
    "",
    response_model=list[schemas.User],
)
async def get_users(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[models.User]:
    users: list[models.User] = await crud.user.get_multi(
        db,
        skip=skip,
        limit=limit,
    )

    return users


@router.post(
    "",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    *,
    user_in: schemas.UserCreate,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
) -> Any:
    user_in_data: dict[str, Any] = jsonable_encoder(user_in)
    user: list[models.User] | None = await crud.user.get_by_kwargs(
        db=db,
        kwargs={"email": user_in_data["email"]},
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with email already exists.",
        )
    user = await crud.user.create(db, obj_in=user_in)
    return user


@router.get(
    "/{id}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    id: int,  # noqa: A002
    db: Annotated[AsyncSession, Depends(deps.get_db)],
) -> Any:
    user: models.User | None = await crud.user.get(db, idx=id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exists.",
        )

    return user


@router.patch(
    "/{id}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    *,
    id: int,  # noqa: A002
    user_in: schemas.UserUpdate,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
) -> Any:
    user: models.User | None = await crud.user.get(db=db, idx=id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exists.",
        )
    user = await crud.user.update(db=db, db_obj=user, obj_in=user_in)

    return user


@router.delete(
    "/{id}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    *,
    id: int,  # noqa: A002
    db: Annotated[AsyncSession, Depends(deps.get_db)],
) -> Any:
    user: models.User | None = await crud.user.get(db=db, idx=id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exists.",
        )
    user = await crud.user.remove(db=db, idx=id)

    return user

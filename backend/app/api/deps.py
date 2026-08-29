from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio.session import AsyncSession

# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt
# from pydantic import ValidationError
# from app import crud, models, schemas
from app.db.session import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, Any, None]:
    async with AsyncSessionLocal() as session:
        yield session

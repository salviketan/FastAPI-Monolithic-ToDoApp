from collections.abc import Generator

# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt
# from pydantic import ValidationError
from sqlalchemy.orm import Session

# from app import crud, models, schemas
from app.db.session import SessionLocal


def get_db() -> Generator:
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()


db_session: Session = next(get_db())

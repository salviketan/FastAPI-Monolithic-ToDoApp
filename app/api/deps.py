from collections.abc import Generator

# from app import crud, models, schemas
from db.session import SessionLocal

# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt
# from pydantic import ValidationError
from sqlalchemy.orm import Session


def get_db() -> Generator:
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()


db_session: Session = next(get_db())

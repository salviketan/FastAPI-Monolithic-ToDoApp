from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.core.config import settings

if settings.ENVIRONMENT == "production":
    engine: Engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
else:
    # 1. Define the directory and ensure it exists
    DB_DIR = Path("local_db")
    DB_DIR.mkdir(parents=True, exist_ok=True)

    engine: Engine = create_engine(
        settings.SQLALCHEMY_DB_URL,
        connect_args={"check_same_thread": False},
    )

SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

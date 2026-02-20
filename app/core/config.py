import os
from pathlib import Path
from typing import Any

from pydantic import AnyHttpUrl, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR: Path = Path(__file__).resolve().parent.parent

env_path: Path = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path,
        case_sensitive=True,
    )

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "To Do App"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    TAGS_METADATA: list[dict[str, str]] = []
    DB_ENGINE: str = os.getenv("DB_ENGINE", "postgresql")
    DB_ENGINE_LIB: str = os.getenv("DB_ENGINE_LIB", "postgresql+psycopg2")
    ROOT_DB_USER: str = os.getenv("ROOT_DB_USER", "")
    ROOT_DB_PASSWORD: str = os.getenv("ROOT_DB_PASSWORD")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME")
    SQLALCHEMY_DB_URL: str = os.getenv(
        "SQLALCHEMY_DB_URL",
        "{engine}://{user}:{passwd}@{host}:{port}/{db}",
    )
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return str(
            PostgresDsn.build(
                scheme=info.data.get("DB_ENGINE"),
                username=info.data.get("DB_USER"),
                password=info.data.get("DB_PASSWORD"),
                host=info.data.get("DB_HOST"),
                port=int(info.data.get("DB_PORT", 5432)),
                path=info.data.get("DB_NAME") or "",
            ),
        )


settings = Settings()

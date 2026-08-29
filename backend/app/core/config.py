import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

BASE_DIR: Path = Path(__file__).resolve().parents[1]

env_path: Path = BASE_DIR.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path,
        case_sensitive=True,
        env_file_encoding="utf-8",
    )

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "To Do App"
    BACKEND_CORS_ORIGINS: list[str] = Field(default=["*"])
    TAGS_METADATA: list[dict[str, str]] = Field(default=[])
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    PYTEST: bool = os.getenv("PYTEST", "False") == "True"

    DB_DRIVER: str = "postgresql+asyncpg"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    APP_DB_USER: str
    APP_DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    POSTGRES_DB: str

    @property
    def SQLALCHEMY_DB_URL(self) -> URL:
        # URL.create() automatically handles escaping special characters like @, :, #, etc.
        return URL.create(
            drivername=self.DB_DRIVER,
            username=self.APP_DB_USER,
            password=self.APP_DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.POSTGRES_DB,
        )


settings = Settings()

from loguru import logger
from pathlib import Path

from pydantic import PrivateAttr, BaseModel
from pydantic_settings import BaseSettings
from typing import AsyncGenerator

from sqlalchemy import NullPool

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from core.config.paths import PathSettings
from core.config.logging import LoggingSettings
from core.utils.singleton import Singleton

BASE_DIR = PathSettings.BASE_DIR

LoggingSettings()

class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        logger.info(f"Creating DB helper with {url=}")
        self.engine = create_async_engine(url=url, echo=echo, poolclass=NullPool)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, str]:
        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                logger.error(f"Database session error: {e}")
                await session.rollback()
                raise


class DataBase(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int

    @property
    def URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = dict(extra="ignore")

class AuthJWT(BaseModel):
    PRIVATE_KEY: Path = PathSettings.PRIVATE_KEY_PATH
    PUBLIC_KEY: Path = PathSettings.PUBLIC_KEY_PATH
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1


class Settings(BaseSettings, Singleton):
    TITLE: str = "Coffee API"
    DESCRIPTION: str = ""
    VERSION: str = "0.1.0"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DOMAIN: str = ""

    @property
    def app_params(self) -> dict:
        return {
            "title": self.TITLE,
            "description": self.DESCRIPTION,
            "version": self.VERSION,
            "swagger_ui_parameters": {"defaultModelsExpandDepth": -1},
            "root_path": "",
        }

    @property
    def uvicorn_params(self) -> dict:
        return {
            "host": self.HOST,
            "port": self.PORT,
            "proxy_headers": True,
            "log_level": "debug",
            "reload": True,
        }

    COOKIE_DOMAIN: str | None = None
    COOKIE_SECURE: bool = True
    COOKIE_SAMESITE: str = "None"

    CORS_ORIGINS: list[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://0.0.0.0:8000",
    ]

    model_config = dict(extra="ignore")
    _db: DataBase = PrivateAttr()
    _db_helper: DatabaseHelper = PrivateAttr()
    _paths: PathSettings = PrivateAttr()
    _auth_jwt: AuthJWT = PrivateAttr()

    def __init__(self, env_file: str | Path | None = None):
        super().__init__(_env_file=env_file)

        db_settings = DataBase(_env_file=env_file)
        self._db: DataBase = db_settings
        self._db_helper: DatabaseHelper = DatabaseHelper(
            url=db_settings.URL_asyncpg, echo=True
        )

        self._paths: PathSettings = PathSettings()
        self._auth_jwt: AuthJWT = AuthJWT()


    @property
    def db(self) -> DataBase:
        return self._db

    @property
    def db_helper(self) -> DatabaseHelper:
        return self._db_helper

    @property
    def paths(self) -> PathSettings:
        return self._paths

    @property
    def auth_jwt(self) -> AuthJWT:
        return self._auth_jwt

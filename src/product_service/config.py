from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic.v1 import BaseSettings


class Config(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    APP_TITLE: str = Field(alias='APP_TITLE')
    APP_VERSION: str = Field(alias='APP_VERSION')
    API_PREFIX: str = Field(alias='API_PREFIX')
    API_VERSION: str = Field(alias='API_VERSION')
    ENVIRONMENT: Literal['dev', 'prod', 'test'] = Field(alias='ENVIRONMENT')
    USER_ACCESS_TOKEN: str = Field(alias='USER_ACCESS_TOKEN')
    USER_ACCESS_TOKEN_SSO: str = Field(alias='USER_ACCESS_TOKEN_SSO')
    LOG_LEVEL: str = Field(alias='LOG_LEVEL')

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    @property
    def database_url(self) -> str:
        return (f'postgresql+asyncpg://'
                f'{self.DB_USER}:{self.DB_PASS}@'
                f'{self.DB_HOST}:{self.DB_PORT}/'
                f'{self.DB_NAME}')

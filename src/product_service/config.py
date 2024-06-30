import os
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 5

    APP_TITLE: str = Field(alias='APP_TITLE')
    API_PREFIX: str = Field(alias='API_PREFIX')
    API_VERSION: str = Field(alias='API_VERSION')
    ENVIRONMENT: Literal['dev', 'prod', 'test'] = Field(alias='ENVIRONMENT')
    LOG_LEVEL: str = Field(alias='LOG_LEVEL')

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    @property
    def database_url(self) -> str:
        return (f'postgresql+asyncpg://'
                f'{self.DB_USER}:{self.DB_PASS}@'
                f'{self.DB_HOST}:{self.DB_PORT}/'
                f'{self.DB_NAME}')

    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT.lower() == 'test'


class TestSettings(Settings):

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='TEST_',
    )


class DevSettings(Settings):

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='DEV_',
    )


class ProdSettings(Settings):

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='PROD_',
    )


ENVIRONMENTS: dict[str, type[Settings]] = {
    'test': TestSettings,
    'dev': DevSettings,
    'prod': ProdSettings,
}


def get_settings() -> Settings:
    env = os.environ.get('ENVIRONMENT', 'dev').lower()
    return ENVIRONMENTS[env]()

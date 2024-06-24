import os
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic.v1 import BaseSettings
from pydantic_settings import SettingsConfigDict


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
    LOG_LEVEL: str = Field(alias='LOG_LEVEL')

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    @property
    def database_url(self) -> str:
        return (f'postgresql+asyncpg://'
                f'{self.DB_USER}:{self.DB_PASS}@'
                f'{self.DB_HOST}:{self.DB_PORT}/'
                f'{self.DB_NAME}')


class TestConfig(Config):
    model_config = SettingsConfigDict(
        env_file='.test.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='TEST_',
    )


ENVIRONMENTS: dict[str, type[Config]] = {
    'test': TestConfig,
}


def get_settings() -> Config:
    env = os.environ.get('ENVIRONMENT', 'dev').lower()
    return ENVIRONMENTS[env]()

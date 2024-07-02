from collections.abc import Iterable

from fastapi import APIRouter
from fastapi import FastAPI

from config import get_settings
from config import Settings
from infrastructure.entrypoints.rest_api.products import product_router

settings = get_settings()


def create_app(conf: Settings, routers: Iterable[APIRouter]) -> FastAPI:
    """FastAPI application factory."""

    application = FastAPI(
        title=conf.APP_TITLE,
        version=conf.API_VERSION,
        root_path=f'/{conf.API_PREFIX}/{conf.API_VERSION}',
    )

    for router in routers:
        application.include_router(router)

    return application


app = create_app(settings, [product_router])

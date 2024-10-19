from fastapi import FastAPI

from src.presentation.routers import __routers__


def register_routers(app: FastAPI):
    for router in __routers__:
        app.include_router(router)

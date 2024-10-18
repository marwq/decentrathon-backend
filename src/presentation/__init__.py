from fastapi import FastAPI

from src.presentation.routers.auth import router as auth_router
from src.presentation.routers.applicant import router as applicant_router

routers = [
    auth_router,
    applicant_router,
]


def register_routers(app: FastAPI):
    for router in routers:
        app.include_router(router)

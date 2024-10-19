from src.presentation.routers.auth import router as auth_router
from src.presentation.routers.applicant import router as applicant_router
from src.presentation.routers.recruiter import router as recruiter_router
from src.presentation.routers.job import router as job_router
from src.presentation.routers.user import router as user_router
from src.presentation.routers.application import router as application_router

__routers__ = [
    auth_router,
    applicant_router,
    recruiter_router,
    job_router,
    user_router,
    application_router,
]
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.presentation import register_routers
from src.presentation.utils import app_lifespan, lifespan_redis
from config import settings


app = FastAPI(
    root_path="/api",
    lifespan=app_lifespan(
        lifespans=[lifespan_redis],
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

register_routers(app)


def main():

    import uvicorn

    uvicorn.run(
        "main:app", 
        host="0.0.0.0",
        port=settings.APP_PORT,
        workers=4,
        reload=True,
    )


if __name__ == "__main__":
    main()

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    APP_PORT: int
    MINIAPP_BASE_URL: str

    # Postgres
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: int

    # Pinecone
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    
    # TG
    TELEGRAM_BOT_TOKEN: str
    
    # Redis
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str


settings = Settings()

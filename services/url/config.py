from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    base_url: str = "http://localhost:8002"
    environment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
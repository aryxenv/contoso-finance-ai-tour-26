"""Application configuration via environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Global application settings."""

    app_name: str = "Contoso Finance"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/contoso_finance"

    # Auth
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30

    # CORS
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = {"env_prefix": "CONTOSO_", "env_file": ".env"}


settings = Settings()

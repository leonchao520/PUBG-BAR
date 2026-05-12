from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://pubg:pubg123@localhost:5432/pubg"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # PUBG API
    pubg_api_key: str = ""
    pubg_api_base: str = "https://api.pubg.com"

    # CORS
    cors_origins: str = "http://localhost:3000"

    # Cache TTL (seconds)
    player_cache_ttl: int = 900  # 15 minutes
    season_cache_ttl: int = 600  # 10 minutes

    model_config = {"env_file": "../.env", "env_file_encoding": "utf-8"}


settings = Settings()

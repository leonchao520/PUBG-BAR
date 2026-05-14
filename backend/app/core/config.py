from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PUBG API
    pubg_api_key: str = ""
    pubg_api_base: str = "https://api.pubg.com"

    # Database (optional - dev mode uses mock data)
    database_url: str = ""

    # Redis (optional - dev mode skips cache)
    redis_url: str = ""

    # CORS
    cors_origins: str = "http://localhost:3000"

    # Cache TTL (seconds)
    player_cache_ttl: int = 900  # 15 min - player profile
    season_cache_ttl: int = 1800  # 30 min - season stats
    matches_cache_ttl: int = 600  # 10 min - recent matches
    rankings_cache_ttl: int = 3600  # 1h - rankings

    # Dev mode (no DB/Redis needed)
    dev_mode: bool = True

    model_config = {"env_file": "../.env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    echo_sql: bool = False
    test: bool = False
    project_name: str = "nbsapi"
    oauth_token_secret: str = "secret"
    model_config = SettingsConfigDict(env_file=".env")
    # env vars will always override settings from .env


settings = Settings()  # type: ignore

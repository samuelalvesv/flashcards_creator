from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    VIDEOANKI_URL: str = "https://videoanki.app"
    VIDEOANKI_CSRF_TOKEN: str
    VIDEOANKI_SESSION_ID: str
    VIDEOANKI_COOKIE_HEADER: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()  # type: ignore

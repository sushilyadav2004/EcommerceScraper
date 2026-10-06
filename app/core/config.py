from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "E-commerce Product Scraper"
    APP_ENV: str = "development"

    DB_SERVER: str
    DB_NAME: str
    DB_DRIVER: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
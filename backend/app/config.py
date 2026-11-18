from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./estoque.db"
    jwt_secret: str = "development-secret-change-me"
    jwt_expire_minutes: int = 60
    admin_username: str = "admin"
    admin_password: str = "admin123-change-me"
    cors_origins: str = "http://localhost:4200"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

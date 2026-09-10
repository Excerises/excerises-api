from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_PORT: int = 5000
    LOG_LEVEL: str = "DEBUG"
    DATABASE_URL: str = "mysql+aiomysql://root:@localhost:3306/excerises"
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = {"env_file": ".env"}

    def is_development(self) -> bool:
        return "prod" not in self.APP_ENV


settings = Settings()

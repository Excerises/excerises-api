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

    HF_TOKEN: str = ""
    HF_REPOSITORY: str = ""
    HF_FITNESS_CLASSIFICATION_MODEL_NAME: str = "fitness_svm_model.pkl"
    HF_FITNESS_CLASSIFICATION_SCALER_NAME: str = "fitness_standard_scaler.pkl"
    HF_EXERCISE_RECOMMENDATION_CSV: str = "exercise_recommendation.csv"
    HF_EXERCISE_RECOMMENDATION_MODEL_NAME: str = "exercise_recommendation_knn_model.pkl"
    HF_EXERCISE_RECOMMENDATION_FEATURE_ENCODER_NAME: str = (
        "exercise_recommendation_onehot_features_encoder.pkl"
    )

    AWS_ENDPOINT_URL: str = "http://localhost:9000"
    AWS_ACCESS_KEY_ID: str = "rustfsadmin"
    AWS_SECRET_ACCESS_KEY: str = "rustfsadmin"
    AWS_REGION: str = "asia-east-1"
    AWS_BUCKET_NAME: str = "excerises"

    model_config = {"env_file": ".env"}

    def is_development(self) -> bool:
        return "prod" not in self.APP_ENV


settings = Settings()

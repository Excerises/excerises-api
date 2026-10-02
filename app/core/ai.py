import huggingface_hub as hf
import joblib

from app.core import log
from app.core.config import settings
from app.shared.model.ai import ExerciseRecommendationModel, FitnessClassificationModel

hf.login(settings.HF_TOKEN)

_fitness_model = None
_fitness_scaler = None
_exercise_recommendation_model = None
_exercise_recommendation_feature_encoder = None


def _hub_download(filename: str):
    return hf.hf_hub_download(
        repo_id=settings.HF_REPOSITORY,
        filename=filename,
        cache_dir="./.cache",
    )


def load_fitness_classification_model() -> FitnessClassificationModel:
    global _fitness_model
    global _fitness_scaler

    if _fitness_scaler is None:
        scaler_path = _hub_download(settings.HF_FITNESS_CLASSIFICATION_SCALER_NAME)
        _fitness_scaler = joblib.load(scaler_path)
        log.info("Fitness classification scaler loaded")

    if _fitness_model is None:
        model_path = _hub_download(settings.HF_FITNESS_CLASSIFICATION_MODEL_NAME)
        _fitness_model = joblib.load(model_path)
        log.info("Fitness classification model loaded")

    return FitnessClassificationModel(
        model=_fitness_model,
        scaler=_fitness_scaler,
    )


def load_exercise_recommendation_model() -> ExerciseRecommendationModel:
    global _exercise_recommendation_model
    global _exercise_recommendation_feature_encoder

    if _exercise_recommendation_feature_encoder is None:
        feature_encoder_path = _hub_download(
            settings.HF_EXERCISE_RECOMMENDATION_FEATURE_ENCODER_NAME
        )
        _exercise_recommendation_feature_encoder = joblib.load(feature_encoder_path)
        log.info("Exercise recommendation feature encoder loaded")

    if _exercise_recommendation_model is None:
        model_path = _hub_download(settings.HF_EXERCISE_RECOMMENDATION_MODEL_NAME)
        _exercise_recommendation_model = joblib.load(model_path)
        log.info("Exercise recommendation model loaded")

    return ExerciseRecommendationModel(
        model=_exercise_recommendation_model,
        feature_encoder=_exercise_recommendation_feature_encoder,
    )

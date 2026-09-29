import huggingface_hub as hf
import joblib

from app.core import log
from app.core.config import settings

hf.login(settings.HF_TOKEN)

_fitness_model = None
_fitness_scaler = None


def _hub_download(filename: str):
    return hf.hf_hub_download(
        repo_id=settings.HF_REPOSITORY,
        filename=filename,
        cache_dir="./.cache",
    )


def load_fitness_classification_scaler():
    global _fitness_scaler

    if _fitness_scaler is not None:
        return _fitness_scaler

    scaler_path = _hub_download(settings.HF_FITNESS_CLASSIFICATION_SCALER_NAME)
    _fitness_scaler = joblib.load(scaler_path)
    log.info("Fitness classification scaler loaded")

    return _fitness_scaler


def load_fitness_classification_model():
    global _fitness_model

    if _fitness_model is not None:
        return _fitness_model

    model_path = _hub_download(settings.HF_FITNESS_CLASSIFICATION_MODEL_NAME)
    _fitness_model = joblib.load(model_path)
    log.info("Fitness classification model loaded")

    return _fitness_model

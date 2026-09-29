from dataclasses import dataclass
from typing import Any


@dataclass
class FitnessClassificationModel:
    model: Any
    scaler: Any

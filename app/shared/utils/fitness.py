import numpy as np

from app.core.ai import (
    load_fitness_classification_model,
)
from app.database.schemas import UserProfileGender


def calculate_bmi(height: float, weight: float):
    return weight / ((height / 100) ** 2)


def calculate_fitness_level(
    gender: UserProfileGender,
    age: int,
    height: float,
    weight: float,
    workout_freq_per_week: int,
    workout_duration_per_day: float,
    water_intake_daily: float,
) -> int:
    bmi = calculate_bmi(height, weight)
    gender_normalized = 1 if gender == UserProfileGender.MALE else 0
    data = np.array(
        [
            [
                age,
                gender_normalized,
                weight,
                height,
                water_intake_daily,
                workout_freq_per_week,
                workout_duration_per_day,
                bmi,
            ]
        ]
    )

    p = load_fitness_classification_model()
    model = p.model
    scaler = p.scaler

    data_scaled = scaler.transform(data)

    preds = model.predict(data_scaled)
    probs = model.predict_proba(data_scaled)
    print(probs)

    fitness_level = int(preds[0])

    return fitness_level

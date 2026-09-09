from datetime import date, time

from pydantic import BaseModel


class ProfileResponse(BaseModel):
    id: str
    user_id: str
    birth_date: date | None = None
    height: float | None = None
    weight: float | None = None
    bmi: float | None = None
    workout_freq_per_week: int | None = None
    fitness_level: str | None = None
    reminder_days: list[int] | None = None
    reminder_time: time | None = None
    workout_duration_per_day: int | None = None

    model_config = {"from_attributes": True}


class ProfileUpdateRequest(BaseModel):
    birth_date: date | None = None
    height: float | None = None
    weight: float | None = None
    workout_freq_per_week: int | None = None
    fitness_level: str | None = None
    reminder_days: list[int] | None = None
    reminder_time: time | None = None
    workout_duration_per_day: int | None = None

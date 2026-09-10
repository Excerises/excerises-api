from datetime import date, time

from pydantic import BaseModel, Field

from app.database.schemas import UserRole


class ProfileData(BaseModel):
    id: str
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


class ProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    role: UserRole
    profile: ProfileData | None = None

    model_config = {"from_attributes": True}


class ProfileUpdateRequest(BaseModel):
    birth_date: date | None = None
    height: float | None = None
    weight: float | None = None
    workout_freq_per_week: int | None = None
    reminder_days: list[int] | None = None
    reminder_time: time | None = None
    workout_duration_per_day: int | None = None


class CalculateFitnessLevelRequest(BaseModel):
    pass


class CalculateFitnessLevelResponse(BaseModel):
    level: int = Field(ge=1, le=3)

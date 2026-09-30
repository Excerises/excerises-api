from datetime import date, time

from pydantic import BaseModel, Field

from app.database.schemas import UserProfileGender, UserRole


class ProfileData(BaseModel):
    id: str
    gender: UserProfileGender | None = None
    birth_date: date | None = None
    height: float | None = None
    weight: float | None = None
    bmi: float | None = None
    workout_duration_per_day: float | None = None
    workout_freq_per_week: int | None = None
    reminder_days: list[int] | None = None
    reminder_time: time | None = None
    water_intake_daily: float | None = None
    fitness_level: str | None = None

    model_config = {"from_attributes": True}


class ProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    role: UserRole
    profile: ProfileData | None = None

    model_config = {"from_attributes": True}


class ProfileUpdateRequest(BaseModel):
    gender: UserProfileGender | None = None
    birth_date: date | None = None
    height: float | None = None
    weight: float | None = None
    workout_duration_per_day: float | None = None
    workout_freq_per_week: int | None = None
    reminder_days: list[int] | None = None
    reminder_time: time | None = None
    water_intake_daily: float | None = None


class CalculateFitnessLevelResponse(BaseModel):
    level: str = Field(...)

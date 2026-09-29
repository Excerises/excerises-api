from datetime import date, datetime, time

from pydantic import BaseModel, EmailStr, Field

from app.database.schemas import UserProfileGender, UserRole


class AdminProfileData(BaseModel):
    id: str
    birth_date: date | None = None
    gender: UserProfileGender | None = None
    height: float | None = None
    weight: float | None = None
    bmi: float | None = None
    workout_freq_per_week: int | None = None
    workout_duration_per_day: float | None = None
    water_intake_daily: float | None = None
    reminder_days: list[int] | None = None
    reminder_time: time | None = None
    fitness_level: str | None = None

    model_config = {"from_attributes": True}


class AdminUserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: UserRole
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class AdminUserDetailResponse(AdminUserResponse):
    profile: AdminProfileData | None = None


class AdminUserCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: UserRole = UserRole.USER


class AdminUserAuthUpdateRequest(BaseModel):
    password: str = Field(min_length=6, max_length=128)


class AdminUserProfileUpdateRequest(BaseModel):
    birth_date: date | None = None
    height: float | None = None
    weight: float | None = None
    workout_freq_per_week: int | None = None
    workout_duration_per_day: float | None = None
    water_intake_daily: float | None = None
    reminder_days: list[int] | None = None
    reminder_time: time | None = None
    fitness_level: str | None = None

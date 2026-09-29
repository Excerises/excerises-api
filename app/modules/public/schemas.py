from pydantic import BaseModel, Field


class PublicCalculateFitnessRequest(BaseModel):
    age: int = Field(ge=1, le=120)
    height: float = Field(gt=0)
    weight: float = Field(gt=0)
    bmi: float = Field(gt=0)
    workout_freq_per_week: int = Field(ge=0, le=7)
    workout_duration_per_day: int = Field(ge=0)


class PublicCalculateFitnessResponse(BaseModel):
    level: int = Field(ge=1, le=3)

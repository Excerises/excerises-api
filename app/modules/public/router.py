from fastapi import APIRouter

from app.shared.model import ApiResponse, api_response
from app.shared.utils.fitness import calculate_fitness_level

from .schemas import PublicCalculateFitnessRequest, PublicCalculateFitnessResponse

router = APIRouter(tags=["Public"])


@router.post(
    "/calculate-fitness",
    response_model=ApiResponse[PublicCalculateFitnessResponse],
    summary="Calculate fitness level",
)
async def public_calculate_fitness(body: PublicCalculateFitnessRequest):
    level = calculate_fitness_level(
        gender=body.gender,
        age=body.age,
        height=body.height,
        weight=body.weight,
        workout_freq_per_week=body.workout_freq_per_week,
        workout_duration_per_day=body.workout_duration_per_day,
        water_intake_daily=body.water_intake_daily,
    )
    return api_response("fitness level calculated", {"level": level})

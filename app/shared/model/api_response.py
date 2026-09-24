from pydantic import BaseModel


class ApiResponse[T](BaseModel):
    message: str
    data: T


def api_response[T](message: str, data: T) -> ApiResponse[T]:
    return ApiResponse(
        message=message,
        data=data,
    )

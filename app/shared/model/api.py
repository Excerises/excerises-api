from typing import Any
from fastapi import Request
from pydantic import BaseModel


class ApiRequest(Request):
    id: None | str
    user_id: None | Any


class ApiResponse[T](BaseModel):
    message: str
    data: T


def api_response[T](message: str, data: T) -> ApiResponse[T]:
    return ApiResponse(
        message=message,
        data=data,
    )

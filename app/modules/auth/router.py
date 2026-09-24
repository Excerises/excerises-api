from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.shared.model import api_response, ApiResponse

from .schemas import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse
from .service import login, refresh_token, register

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[Any]
)
async def register_user(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    try:
        user = await register(db, body.name, body.email, body.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return api_response(
        "register success",
        {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role.value,
        },
    )


@router.post("/login", response_model=ApiResponse[TokenResponse])
async def login_user(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        tokens = await login(db, body.email, body.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return api_response("login success", tokens)


@router.post("/refresh", response_model=ApiResponse[TokenResponse])
async def refresh_tokens(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    try:
        tokens = await refresh_token(db, body.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return api_response("refresh token success", tokens)

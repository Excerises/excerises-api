from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.database.schemas import User
from app.modules.auth.dependencies import require_admin
from app.modules.news.schemas import (
    NewsCreateRequest,
    NewsResponse,
    NewsUpdateRequest,
)
from app.modules.news.service import (
    create_news,
    delete_news,
    get_news,
    list_news,
    update_news,
)
from app.shared.model import ApiResponse, api_response

router = APIRouter(
    prefix="/admin/news",
    tags=["Admin - News"],
    dependencies=[Depends(require_admin)],
)


@router.get("", response_model=ApiResponse[list[NewsResponse]])
async def admin_list_news(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return api_response("list news fetched", await list_news(db))


@router.post(
    "", response_model=ApiResponse[NewsResponse], status_code=status.HTTP_201_CREATED
)
async def admin_create_news(
    body: NewsCreateRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    news = await create_news(
        db, body.title, body.description, body.content, str(admin.id)
    )
    return api_response(
        "news successfully created",
        news,
    )


@router.get("/{news_id}", response_model=ApiResponse[NewsResponse])
async def admin_get_news(
    news_id: str,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    news = await get_news(db, news_id)
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="News not found"
        )
    return api_response("news fetched", news)


@router.put("/{news_id}", response_model=ApiResponse[NewsResponse])
async def admin_update_news(
    news_id: str,
    body: NewsUpdateRequest,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    data = body.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update"
        )
    news = await update_news(db, news_id, data)
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="News not found"
        )
    return api_response("news updated", news)


@router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_news(
    news_id: str,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    ok = await delete_news(db, news_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="News not found"
        )
    return api_response("news deleted")

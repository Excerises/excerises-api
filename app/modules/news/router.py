from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db

from .schemas import NewsResponse
from .service import get_public_news, list_news

router = APIRouter(prefix="/news", tags=["News"])


@router.get("", response_model=list[NewsResponse])
async def public_list_news(db: AsyncSession = Depends(get_db)):
    return await list_news(db)


@router.get("/{news_id}", response_model=NewsResponse)
async def public_get_news(news_id: str, db: AsyncSession = Depends(get_db)):
    news = await get_public_news(db, news_id)
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="News not found"
        )
    return news

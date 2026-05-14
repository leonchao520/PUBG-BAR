from fastapi import APIRouter, Depends, Query

from app.core.database import get_db
from app.core.redis import get_redis
from app.services.ranking_service import RankingService

router = APIRouter(prefix="/api/rankings", tags=["rankings"])


@router.get("")
async def get_rankings(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db=Depends(get_db),
    redis=Depends(get_redis),
):
    """获取排行榜"""
    service = RankingService(db, redis)
    data = await service.get_rankings(page=page, page_size=page_size)
    return {"data": data}

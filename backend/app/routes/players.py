from fastapi import APIRouter, Depends
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.redis import get_redis
from app.services.player_service import PlayerService

router = APIRouter(prefix="/api/players", tags=["players"])


@router.get("/{name}")
async def get_player(
    name: str,
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    """获取玩家数据（含缓存）"""
    service = PlayerService(db, redis)
    data = await service.get_player(name)
    if data is None:
        return {"error": "Player not found", "code": 404}
    return {"data": data}


@router.get("/search")
async def search_players(
    q: str,
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    """搜索玩家"""
    service = PlayerService(db, redis)
    results = await service.search_players(q)
    return {"data": results}

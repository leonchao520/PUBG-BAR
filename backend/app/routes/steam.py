from fastapi import APIRouter

from app.core.config import settings
from app.services.steam_service import SteamService

router = APIRouter(prefix="/api/steam", tags=["steam"])


@router.get("/{steam_id}")
async def get_steam_info(steam_id: str):
    """获取 Steam 玩家信息（头像/封禁/游戏时长）"""
    if not settings.steam_api_key:
        return {
            "error": "Steam API Key not configured",
            "code": 503,
        }

    service = SteamService()
    data = await service.get_player_info(steam_id)
    return {"data": data}


@router.get("/{steam_id}/profile")
async def get_steam_profile(steam_id: str):
    """获取 Steam 玩家摘要信息"""
    service = SteamService()
    data = await service.get_player_summaries(steam_id)
    return {"data": data}


@router.get("/{steam_id}/bans")
async def get_steam_bans(steam_id: str):
    """获取 Steam 玩家封禁状态"""
    service = SteamService()
    data = await service.get_player_bans(steam_id)
    return {"data": data}


@router.get("/{steam_id}/pubg")
async def get_steam_pubg(steam_id: str):
    """获取 Steam 玩家 PUBG 游戏时长"""
    service = SteamService()
    data = await service.get_pubg_playtime(steam_id)
    return {"data": data}

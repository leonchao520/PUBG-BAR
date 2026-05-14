"""Steam API 服务
提供玩家 Steam 信息查询：
- 玩家摘要（头像/昵称/个人资料）
- 封禁状态（VAC/游戏封禁）
- 游戏时长（PUBG 游玩时间）
"""

import asyncio
from datetime import datetime

import httpx

from app.core.config import settings

STEAM_API_BASE = "https://api.steampowered.com"
PUBG_APP_ID = "578080"


class SteamService:
    """Steam Web API 封装"""

    def __init__(self):
        self.api_key = settings.steam_api_key
        self.base_url = STEAM_API_BASE

    async def get_player_summaries(self, steam_id: str) -> dict | None:
        """获取玩家 Steam 摘要信息（头像、昵称、个人资料）"""
        if not self.api_key:
            return None

        url = f"{self.base_url}/ISteamUser/GetPlayerSummaries/v0002/"
        params = {"key": self.api_key, "steamids": steam_id}

        async with httpx.AsyncClient(timeout=10) as client:
            try:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
                players = data.get("response", {}).get("players", [])
                if not players:
                    return None
                p = players[0]
                return {
                    "steam_id": p.get("steamid"),
                    "name": p.get("personaname"),
                    "avatar": p.get("avatarfull"),
                    "avatar_medium": p.get("avatarmedium"),
                    "profile_url": p.get("profileurl"),
                    "real_name": p.get("realname"),
                    "country": p.get("loccountrycode"),
                    "created_at": datetime.fromtimestamp(p.get("timecreated", 0)).isoformat() if p.get("timecreated") else None,
                }
            except httpx.HTTPError as e:
                print(f"Steam GetPlayerSummaries error: {e}")
                return None

    async def get_player_bans(self, steam_id: str) -> dict | None:
        """获取玩家封禁状态（VAC/游戏封禁/社区封禁）"""
        if not self.api_key:
            return None

        url = f"{self.base_url}/ISteamUser/GetPlayerBans/v0001/"
        params = {"key": self.api_key, "steamids": steam_id}

        async with httpx.AsyncClient(timeout=10) as client:
            try:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
                bans = data.get("players", [])
                if not bans:
                    return None
                b = bans[0]
                return {
                    "steam_id": b.get("SteamId"),
                    "vac_banned": bool(b.get("VACBanned")),
                    "vac_ban_count": b.get("NumberOfVACBans", 0),
                    "game_bans": b.get("NumberOfGameBans", 0),
                    "community_banned": bool(b.get("CommunityBanned")),
                    "economy_ban": b.get("EconomyBan") != "none" if b.get("EconomyBan") else False,
                    "days_since_last_ban": b.get("DaysSinceLastBan", 0),
                }
            except httpx.HTTPError as e:
                print(f"Steam GetPlayerBans error: {e}")
                return None

    async def get_pubg_playtime(self, steam_id: str) -> dict | None:
        """获取玩家 PUBG 游戏时长"""
        if not self.api_key:
            return None

        url = f"{self.base_url}/IPlayerService/GetOwnedGames/v0001/"
        params = {
            "key": self.api_key,
            "steamid": steam_id,
            "include_appinfo": True,
            "include_played_free_games": True,
            "appids_filter[0]": PUBG_APP_ID,
        }

        async with httpx.AsyncClient(timeout=10) as client:
            try:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
                games = data.get("response", {}).get("games", [])
                if not games:
                    return None
                g = games[0]
                playtime_forever = g.get("playtime_forever", 0)
                playtime_2weeks = g.get("playtime_2weeks", 0)
                return {
                    "app_id": PUBG_APP_ID,
                    "name": g.get("name", "PLAYERUNKNOWN'S BATTLEGROUNDS"),
                    "playtime_forever_minutes": playtime_forever,
                    "playtime_forever_hours": round(playtime_forever / 60, 1),
                    "playtime_2weeks_minutes": playtime_2weeks,
                    "playtime_2weeks_hours": round(playtime_2weeks / 60, 1),
                    "logo_url": f"https://media.steampowered.com/steamcommunity/public/images/apps/{PUBG_APP_ID}/{g.get('img_logo_url', '')}.jpg" if g.get("img_logo_url") else None,
                }
            except httpx.HTTPError as e:
                print(f"Steam GetOwnedGames error: {e}")
                return None

    async def get_player_info(self, steam_id: str) -> dict:
        """获取玩家 Steam 完整信息（汇总）"""
        summaries, bans, playtime = await asyncio.gather(
            self.get_player_summaries(steam_id),
            self.get_player_bans(steam_id),
            self.get_pubg_playtime(steam_id),
        )
        return {
            "steam_id": steam_id,
            "profile": summaries,
            "bans": bans,
            "pubg_playtime": playtime,
        }

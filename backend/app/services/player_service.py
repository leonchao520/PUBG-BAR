import json
from datetime import datetime

import httpx
from redis import asyncio as aioredis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.player import MatchRecord, Player


class PlayerService:
    """玩家数据处理服务"""

    def __init__(self, db: AsyncSession, redis: aioredis.Redis):
        self.db = db
        self.redis = redis

    async def get_player(self, name: str) -> dict | None:
        """获取玩家数据，缓存策略：Redis → DB → PUBG API"""

        # 1. 查 Redis 缓存
        cached = await self.redis.get(f"player:{name.lower()}")
        if cached:
            return json.loads(cached)

        # 2. 查 DB
        result = await self.db.execute(
            select(Player).where(Player.name.ilike(name))
        )
        player = result.scalar_one_or_none()

        # 3. 如果 DB 数据太旧或没有，调 PUBG API
        if player is None or self._is_stale(player.last_updated):
            api_data = await self._fetch_from_pubg(name)
            if api_data:
                player = await self._save_player(api_data)
                await self._save_recent_matches(player.id, api_data.get("matches", []))

        if player is None:
            return None

        # 构造返回数据
        data = self._build_player_data(player)
        # 写 Redis 缓存（15分钟）
        await self.redis.setex(
            f"player:{name.lower()}",
            settings.player_cache_ttl,
            json.dumps(data, default=str),
        )
        return data

    def _is_stale(self, updated_at: datetime | None) -> bool:
        if updated_at is None:
            return True
        delta = (datetime.utcnow() - updated_at).total_seconds()
        return delta > settings.player_cache_ttl

    async def _fetch_from_pubg(self, name: str) -> dict | None:
        """调 PUBG API 获取玩家数据"""
        headers = {
            "Authorization": f"Bearer {settings.pubg_api_key}",
            "Accept": "application/vnd.api+json",
        }
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                # 搜索玩家
                resp = await client.get(
                    f"{settings.pubg_api_base}/shards/steam/players",
                    params={"filter[playerNames]": name},
                    headers=headers,
                )
                resp.raise_for_status()
                data = resp.json()

                players = data.get("data", [])
                if not players:
                    return None

                player_data = players[0]
                return {
                    "id": player_data["id"],
                    "name": player_data["attributes"].get("name", name),
                    "platform": "steam",
                    "level": player_data["attributes"].get("level", 0),
                    "avatar_url": player_data["attributes"].get("avatar"),
                }
            except httpx.HTTPError as e:
                print(f"PUBG API error: {e}")
                return None

    async def _save_player(self, data: dict) -> Player:
        """保存或更新玩家到 DB"""
        player = Player(
            id=data["id"],
            name=data["name"],
            platform=data.get("platform", "steam"),
            level=data.get("level", 0),
            avatar_url=data.get("avatar_url"),
            last_updated=datetime.utcnow(),
        )
        # upsert
        await self.db.merge(player)
        await self.db.flush()
        return player

    async def _save_recent_matches(self, player_id: str, matches: list):
        """保存最近比赛记录（预留）"""
        # TODO: 根据 PUBG API 格式解析比赛数据
        pass

    def _build_player_data(self, player: Player) -> dict:
        """构造返回给前端的玩家数据"""
        return {
            "id": player.id,
            "name": player.name,
            "platform": player.platform,
            "level": player.level,
            "avatar_url": player.avatar_url,
            "clan_name": player.clan_name,
            "season": None,   # 赛季数据后续补充
            "recent_matches": [
                {
                    "id": m.id,
                    "mode": m.game_mode,
                    "kills": m.kills,
                    "damage": m.damage,
                    "win": bool(m.is_win),
                    "time": m.created_at.isoformat() if m.created_at else None,
                }
                for m in (player.matches or [])
            ],
        }

    async def search_players(self, query: str) -> list[dict]:
        """搜索玩家（从 DB 和 PUBG API）"""
        result = await self.db.execute(
            select(Player).where(Player.name.ilike(f"%{query}%")).limit(20)
        )
        players = result.scalars().all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "platform": p.platform,
                "level": p.level,
            }
            for p in players
        ]

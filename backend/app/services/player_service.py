import json
from datetime import datetime, timedelta

import httpx

from app.core.config import settings

# Mock data for dev mode (no DB/Redis)
MOCK_PLAYERS = {
    "shrimpyking": {
        "id": "mock-account-001",
        "name": "ShrimpyKing",
        "platform": "steam",
        "level": 500,
        "avatar_url": None,
        "clan_name": "SHRIMP",
        "season": {
            "kd": 4.52,
            "winRate": 18.3,
            "top10Rate": 35.7,
            "games": 248,
            "avgDamage": 385,
            "bestRank": 12,
            "tier": "Master",
        },
        "recent_matches": [
            {"id": "m1", "mode": "squad-fpp", "kills": 12, "damage": 1845.5, "win": True, "time": (datetime.utcnow() - timedelta(hours=1)).isoformat()},
            {"id": "m2", "mode": "squad-fpp", "kills": 5, "damage": 823.2, "win": False, "time": (datetime.utcnow() - timedelta(hours=3)).isoformat()},
            {"id": "m3", "mode": "duo-fpp", "kills": 8, "damage": 1204.1, "win": True, "time": (datetime.utcnow() - timedelta(hours=5)).isoformat()},
            {"id": "m4", "mode": "solo-fpp", "kills": 3, "damage": 456.7, "win": False, "time": (datetime.utcnow() - timedelta(hours=8)).isoformat()},
            {"id": "m5", "mode": "squad-fpp", "kills": 15, "damage": 2100.3, "win": True, "time": (datetime.utcnow() - timedelta(hours=10)).isoformat()},
        ],
    },
    "pubgstarmaster": {
        "id": "mock-account-002",
        "name": "PUBGStarMaster",
        "platform": "steam",
        "level": 320,
        "avatar_url": None,
        "clan_name": None,
        "season": {
            "kd": 3.21,
            "winRate": 12.5,
            "top10Rate": 28.3,
            "games": 156,
            "avgDamage": 295,
            "bestRank": 8,
            "tier": "Diamond",
        },
        "recent_matches": [
            {"id": "m6", "mode": "squad-fpp", "kills": 7, "damage": 1100.0, "win": False, "time": (datetime.utcnow() - timedelta(hours=2)).isoformat()},
            {"id": "m7", "mode": "squad-fpp", "kills": 10, "damage": 1560.8, "win": True, "time": (datetime.utcnow() - timedelta(hours=4)).isoformat()},
            {"id": "m8", "mode": "duo-fpp", "kills": 4, "damage": 680.3, "win": False, "time": (datetime.utcnow() - timedelta(hours=6)).isoformat()},
        ],
    },
}


class PlayerService:
    """玩家数据处理服务"""

    def __init__(self, db=None, redis=None):
        self.db = db
        self.redis = redis

    def _find_player(self, name: str) -> dict | None:
        """在 mock 数据中查找玩家（dev mode）"""
        name_lower = name.lower()
        data = MOCK_PLAYERS.get(name_lower)
        if data:
            return data
        for key, val in MOCK_PLAYERS.items():
            if name_lower in key or key in name_lower:
                return val
        return None

    async def get_player(self, name: str) -> dict | None:
        """获取玩家数据（含赛季 + 比赛）"""
        name_lower = name.lower()

        if settings.dev_mode:
            return self._find_player(name)

        # Production mode: Redis → DB → PUBG API
        if self.redis:
            cached = await self.redis.get(f"player:{name_lower}")
            if cached:
                return json.loads(cached)

        api_data = await self._fetch_from_pubg(name)
        if api_data:
            if self.redis:
                await self.redis.setex(
                    f"player:{name_lower}",
                    settings.player_cache_ttl,
                    json.dumps(api_data, default=str),
                )
            return api_data

        return None

    async def get_player_season(self, name: str) -> dict | None:
        """获取玩家赛季数据"""
        name_lower = name.lower()

        if settings.dev_mode:
            player = self._find_player(name)
            if player and player.get("season"):
                return player["season"]
            return None

        # Production: check cache first
        if self.redis:
            cached = await self.redis.get(f"player_season:{name_lower}")
            if cached:
                return json.loads(cached)

        headers = self._pubg_headers()
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                pid = await self._resolve_player_id(name, headers, client)
                if not pid:
                    return None

                data = await self._fetch_season_data(pid, headers, client)
                if data and self.redis:
                    await self.redis.setex(
                        f"player_season:{name_lower}",
                        settings.season_cache_ttl,
                        json.dumps(data, default=str),
                    )
                return data
            except httpx.HTTPError:
                return None

    async def get_player_matches(self, name: str) -> list | None:
        """获取玩家最近比赛记录"""
        name_lower = name.lower()

        if settings.dev_mode:
            player = self._find_player(name)
            if player and player.get("recent_matches"):
                return player["recent_matches"]
            return None

        if self.redis:
            cached = await self.redis.get(f"player_matches:{name_lower}")
            if cached:
                return json.loads(cached)

        headers = self._pubg_headers()
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                pid = await self._resolve_player_id(name, headers, client)
                if not pid:
                    return None

                matches = await self._fetch_match_list(pid, headers, client)
                if matches and self.redis:
                    await self.redis.setex(
                        f"player_matches:{name_lower}",
                        settings.matches_cache_ttl,
                        json.dumps(matches, default=str),
                    )
                return matches
            except httpx.HTTPError:
                return None

    def _pubg_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {settings.pubg_api_key}",
            "Accept": "application/vnd.api+json",
        }

    async def _resolve_player_id(self, name: str, headers: dict, client: httpx.AsyncClient) -> str | None:
        """通过昵称解析 PUBG player ID"""
        try:
            resp = await client.get(
                f"{settings.pubg_api_base}/shards/steam/players",
                params={"filter[playerNames]": name},
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()
            players = data.get("data", [])
            return players[0]["id"] if players else None
        except httpx.HTTPError:
            return None

    async def _fetch_from_pubg(self, name: str) -> dict | None:
        """调 PUBG API 获取玩家数据"""
        headers = self._pubg_headers()
        async with httpx.AsyncClient(timeout=15) as client:
            try:
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

                p = players[0]
                pid = p["id"]
                attrs = p.get("attributes", {})

                season_data = await self._fetch_season_data(pid, headers, client)
                matches = await self._fetch_match_list(pid, headers, client)

                return {
                    "id": pid,
                    "name": attrs.get("name", name),
                    "platform": "steam",
                    "level": attrs.get("level", 0),
                    "avatar_url": attrs.get("avatar"),
                    "clan_name": None,
                    "season": season_data,
                    "recent_matches": matches,
                }
            except httpx.HTTPError as e:
                print(f"PUBG API error: {e}")
                return None

    async def _fetch_season_data(self, player_id: str, headers: dict, client: httpx.AsyncClient) -> dict | None:
        """获取赛季数据"""
        try:
            resp = await client.get(
                f"{settings.pubg_api_base}/shards/steam/players/{player_id}/seasons/lifetime",
                headers=headers,
            )
            resp.raise_for_status()
            raw = resp.json()

            # Parse PUBG API season response
            attrs = raw.get("data", {}).get("attributes", {})
            game_mode_stats = attrs.get("gameModeStats", {})

            # Aggregate across all modes (solo, duo, squad)
            total_kills = 0
            total_deaths = 0
            total_wins = 0
            total_games = 0
            total_top10 = 0
            total_damage = 0.0
            total_rounds_played = 0

            for mode, stats in game_mode_stats.items():
                total_kills += stats.get("kills", 0)
                total_deaths += stats.get("deaths", 0) or 1
                total_wins += stats.get("wins", 0)
                total_games += stats.get("roundsPlayed", 0)
                total_top10 += stats.get("top10s", 0)
                total_damage += stats.get("damageDealt", 0.0)
                total_rounds_played += stats.get("roundsPlayed", 0)

            if total_games == 0:
                return None

            kd = round(total_kills / max(total_deaths, 1), 2)
            win_rate = round((total_wins / total_games) * 100, 1)
            top10_rate = round((total_top10 / total_games) * 100, 1)
            avg_damage = round(total_damage / max(total_games, 1), 1)

            return {
                "kd": kd,
                "winRate": win_rate,
                "top10Rate": top10_rate,
                "games": total_games,
                "avgDamage": avg_damage,
                "bestRank": self._estimate_best_rank(total_kills, total_games),
                "tier": self._estimate_tier(kd, win_rate),
            }
        except httpx.HTTPError as e:
            print(f"Season API error: {e}")
            return None

    async def _fetch_match_list(self, player_id: str, headers: dict, client: httpx.AsyncClient) -> list:
        """获取最近比赛列表"""
        try:
            resp = await client.get(
                f"{settings.pubg_api_base}/shards/steam/players/{player_id}/matches",
                headers=headers,
            )
            resp.raise_for_status()
            raw = resp.json()

            match_ids = [m["id"] for m in raw.get("data", [])][:20]

            # Fetch match details (PUBG API requires individual match fetch)
            matches = []
            for mid in match_ids[:10]:  # Limit to 10 to avoid too many requests
                try:
                    m_resp = await client.get(
                        f"{settings.pubg_api_base}/shards/steam/matches/{mid}",
                        headers=headers,
                    )
                    m_resp.raise_for_status()
                    match_data = m_resp.json()

                    parsed = self._parse_match(mid, match_data, player_id)
                    if parsed:
                        matches.append(parsed)
                except httpx.HTTPError:
                    continue

            return matches
        except httpx.HTTPError as e:
            print(f"Match list API error: {e}")
            return []

    def _parse_match(self, mid: str, match_data: dict, player_id: str) -> dict | None:
        """解析单场比赛数据"""
        included = match_data.get("included", [])
        rosters = [i for i in included if i.get("type") == "roster"]
        participants = [i for i in included if i.get("type") == "participant"]

        # Find the participant matching our player
        our_stats = None
        for p in participants:
            p_attrs = p.get("attributes", {}).get("stats", {})
            if p_attrs.get("playerId") == player_id:
                our_stats = p_attrs
                break

        if not our_stats:
            return None

        # Determine win - find the winning roster
        win = False
        for roster in rosters:
            roster_attrs = roster.get("attributes", {}).get("stats", {})
            if roster_attrs.get("rank") == 1:
                roster_teams = roster.get("relationships", {}).get("participants", {}).get("data", [])
                for team in roster_teams:
                    if team.get("id") == player_id:
                        win = True

        # Get the match asset for game mode
        assets = [i for i in included if i.get("type") == "asset"]
        match_attrs = match_data.get("data", {}).get("attributes", {})
        game_mode = match_attrs.get("gameMode", "unknown")

        return {
            "id": mid,
            "mode": game_mode,
            "kills": our_stats.get("kills", 0),
            "damage": our_stats.get("damageDealt", 0.0),
            "win": win,
            "time": match_attrs.get("createdAt", ""),
            "winPlace": our_stats.get("winPlace", 0),
            "assists": our_stats.get("assists", 0),
            "duration": our_stats.get("timeSurvived", 0),
        }

    def _estimate_best_rank(self, kills: int, games: int) -> int:
        """估算最佳排名（基于 kill 和场次比例）"""
        if games < 50:
            return 0
        ratio = kills / max(games, 1)
        if ratio > 5:
            return 1
        elif ratio > 3:
            return 3
        elif ratio > 2:
            return 8
        else:
            return 15

    def _estimate_tier(self, kd: float, win_rate: float) -> str:
        """根据 KD/胜率估算段位"""
        if kd >= 5 and win_rate >= 20:
            return "Conqueror"
        elif kd >= 4 and win_rate >= 15:
            return "Master"
        elif kd >= 3 and win_rate >= 10:
            return "Diamond"
        elif kd >= 2 and win_rate >= 7:
            return "Platinum"
        elif kd >= 1.5 and win_rate >= 4:
            return "Gold"
        elif kd >= 1:
            return "Silver"
        else:
            return "Bronze"

    async def search_players(self, query: str) -> list[dict]:
        """搜索玩家"""
        query_lower = query.lower()

        if settings.dev_mode:
            return [
                {"id": v["id"], "name": v["name"], "platform": v["platform"], "level": v["level"]}
                for k, v in MOCK_PLAYERS.items()
                if query_lower in k or query_lower in v["name"].lower()
            ]

        # Production: search via PUBG API
        try:
            headers = self._pubg_headers()
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(
                    f"{settings.pubg_api_base}/shards/steam/players",
                    params={"filter[playerNames]": query},
                    headers=headers,
                )
                resp.raise_for_status()
                data = resp.json()
                return [
                    {
                        "id": p["id"],
                        "name": p["attributes"].get("name", ""),
                        "platform": "steam",
                        "level": p["attributes"].get("level", 0),
                    }
                    for p in data.get("data", [])
                ]
        except httpx.HTTPError:
            return []

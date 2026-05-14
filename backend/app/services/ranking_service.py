"""排行榜服务"""

from app.core.config import settings

# Mock rankings data (dev mode)
MOCK_RANKINGS = [
    {"rank": 1, "name": "ShrimpyKing", "level": 500, "kd": 4.52, "winRate": 18.3, "tier": "Master", "games": 248},
    {"rank": 2, "name": "PUBGStarMaster", "level": 320, "kd": 3.21, "winRate": 12.5, "tier": "Diamond", "games": 156},
    {"rank": 3, "name": "NightOwl99", "level": 280, "kd": 2.85, "winRate": 10.2, "tier": "Diamond", "games": 189},
    {"rank": 4, "name": "AceSniper", "level": 450, "kd": 4.10, "winRate": 16.8, "tier": "Master", "games": 312},
    {"rank": 5, "name": "TacticalWolve", "level": 210, "kd": 2.45, "winRate": 9.1, "tier": "Platinum", "games": 178},
    {"rank": 6, "name": "BulletStorm", "level": 380, "kd": 3.80, "winRate": 14.2, "tier": "Diamond", "games": 205},
    {"rank": 7, "name": "CQB_Master", "level": 195, "kd": 2.10, "winRate": 8.5, "tier": "Platinum", "games": 134},
    {"rank": 8, "name": "GhostReaper", "level": 520, "kd": 4.80, "winRate": 20.1, "tier": "Master", "games": 420},
    {"rank": 9, "name": "SteelBeast", "level": 160, "kd": 1.95, "winRate": 7.3, "tier": "Gold", "games": 98},
    {"rank": 10, "name": "FragMasterX", "level": 340, "kd": 3.15, "winRate": 11.9, "tier": "Diamond", "games": 167},
    {"rank": 11, "name": "ShadowStrike", "level": 290, "kd": 2.88, "winRate": 10.5, "tier": "Platinum", "games": 143},
    {"rank": 12, "name": "IronSight", "level": 180, "kd": 2.05, "winRate": 7.8, "tier": "Gold", "games": 112},
    {"rank": 13, "name": "ViperSnake", "level": 260, "kd": 2.65, "winRate": 9.8, "tier": "Platinum", "games": 156},
    {"rank": 14, "name": "WildCard_7", "level": 410, "kd": 3.95, "winRate": 15.6, "tier": "Diamond", "games": 278},
    {"rank": 15, "name": "Blitzkrieg", "level": 140, "kd": 1.80, "winRate": 6.5, "tier": "Gold", "games": 87},
]


class RankingService:
    """排行榜服务"""

    def __init__(self, db=None, redis=None):
        self.db = db
        self.redis = redis

    async def get_rankings(self, page: int = 1, page_size: int = 20) -> dict:
        """获取排行榜"""
        if settings.dev_mode:
            start = (page - 1) * page_size
            end = start + page_size
            items = MOCK_RANKINGS[start:end]
            return {
                "items": items,
                "total": len(MOCK_RANKINGS),
                "page": page,
                "page_size": page_size,
            }

        # Production: query from DB
        # TODO: implement DB-based rankings
        return {"items": [], "total": 0, "page": page, "page_size": page_size}

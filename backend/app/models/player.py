from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(String, primary_key=True, comment="PUBG account ID")
    name = Column(String(64), index=True, nullable=False, comment="游戏昵称")
    platform = Column(String(16), nullable=False, comment="平台: steam/xbox/psn")
    level = Column(Integer, default=0, comment="等级")
    avatar_url = Column(String(256), nullable=True, comment="头像 URL")
    clan_name = Column(String(64), nullable=True, comment="战队名")
    last_updated = Column(DateTime, default=datetime.utcnow, comment="最后更新时间")

    matches = relationship("MatchRecord", back_populates="player", lazy="selectin")


class MatchRecord(Base):
    __tablename__ = "match_records"

    id = Column(String, primary_key=True, comment="比赛 ID")
    player_id = Column(String, ForeignKey("players.id"), index=True, nullable=False)
    game_mode = Column(String(16), nullable=False, comment="模式: solo/duo/squad")
    match_type = Column(String(32), nullable=True, comment="比赛类型: normal/ranked")
    kills = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    damage = Column(Float, default=0.0)
    win_place = Column(Integer, default=0, comment="排名")
    duration = Column(Integer, default=0, comment="持续时间(秒)")
    is_win = Column(Integer, default=0, comment="是否吃鸡")
    created_at = Column(DateTime, default=datetime.utcnow, comment="比赛时间")

    player = relationship("Player", back_populates="matches")

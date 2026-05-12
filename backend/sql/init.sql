-- PUBG Plus 数据库初始化
-- 表结构由 SQLAlchemy ORM 自动创建
-- 这里放一些初始数据和索引

-- 创建扩展
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- 用于模糊搜索玩家名

-- 创建搜索索引（加速 ILIKE 查询）
CREATE INDEX IF NOT EXISTS idx_players_name_trgm ON players USING gin (name gin_trgm_ops);

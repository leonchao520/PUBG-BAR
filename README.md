# PUBG Plus 🦐

PUBG 玩家数据查询工具。Nuxt 3 + FastAPI + PostgreSQL + Redis，全 Docker 部署。

## 架构

```
用户请求 → Nginx → Nuxt 3 (SSR/ISR)
                ↘ FastAPI BFF → Redis (缓存)
                              → PostgreSQL (持久化)
                              → PUBG API (数据源)
```

## 快速启动

### 1. 准备环境

```bash
cp .env.example .env
# 编辑 .env，填入你的 PUBG API Key
```

### 2. 创建 SSL 证书（生产环境）

```bash
mkdir ssl
# 把证书放到 ssl/fullchain.pem 和 ssl/privkey.pem
```

开发环境可以用自签名证书或直接用 HTTP。

### 3. 启动

```bash
# 首次构建并启动
./scripts/deploy.sh --build

# 查看日志
./scripts/deploy.sh --logs

# 停止
./scripts/deploy.sh --stop

# 更新代码后重新部署
./scripts/deploy.sh --update
```

### 4. 访问

- 前端：http://localhost
- API：http://localhost/api
- 健康检查：http://localhost/health

## 本地开发

### 前端（Nuxt 3）

```bash
cd frontend
npm install
npm run dev      # http://localhost:3000
```

### 后端（FastAPI）

```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
# http://localhost:8000
# API 文档: http://localhost:8000/docs
```

启动本地服务前，确保 PostgreSQL 和 Redis 在运行：

```bash
# 只启动依赖服务
docker compose up postgres redis -d
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `PUBG_API_KEY` | [Steam PUBG API Key](https://steamcommunity.com/dev/apikey)（必填） | `3CFD8B32...` |
| `DB_PASSWORD` | 数据库密码 | `pubg123` |
| `DOMAIN` | 部署域名 | `pubg.plus` |

## ISR 路由规则

| 路由 | 渲染模式 | 重新验证 |
|------|---------|---------|
| `/` | 静态生成 | 永不 |
| `/search` | SSR | - |
| `/player/**` | ISR | 30分钟 |
| `/rankings/**` | ISR | 1小时 |

## 项目结构

```
pubg-plus/
├── frontend/          # Nuxt 3 (SSR/ISR)
│   ├── pages/         # 页面路由
│   ├── composables/   # 公共 hooks
│   ├── components/    # 组件
│   └── assets/        # 静态资源
├── backend/           # FastAPI
│   ├── app/
│   │   ├── api/       # 路由
│   │   ├── models/    # SQLAlchemy 模型
│   │   ├── services/  # 业务逻辑层
│   │   └── core/      # 配置/数据库/Redis
│   └── sql/           # SQL 初始化脚本
├── nginx/             # Nginx 配置
├── scripts/           # 部署脚本
└── docker-compose.yml # 全栈编排
```

## Nginx 缓存策略

- **静态资源**：缓存 1 年，hash 文件名不变
- **API GET**：缓存 60s，PUBG 数据不需要实时
- **搜索 API**：不缓存，严格限流（5r/s）
- **全局限流**：30r/s，防止刷 API

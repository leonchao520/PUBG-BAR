#!/bin/bash
set -e

# PUBG Plus 部署脚本
# 用法: ./scripts/deploy.sh [--build] [--env production]

echo "🚀 PUBG Plus Deploy"
echo "==================="

# 检查 .env
if [ ! -f .env ]; then
    echo "⚠️  请先创建 .env 文件（可参考 .env.example）"
    exit 1
fi

# 导出环境变量
set -a
source .env
set +a

# Docker Compose 操作
COMPOSE_CMD="docker compose -f docker-compose.yml"

case "${1:-}" in
    --build)
        echo "🏗️  构建并启动..."
        $COMPOSE_CMD up --build -d
        ;;
    --restart)
        echo "🔄 重启服务..."
        $COMPOSE_CMD restart
        ;;
    --logs)
        echo "📋 查看日志..."
        $COMPOSE_CMD logs -f
        ;;
    --stop)
        echo "🛑 停止服务..."
        $COMPOSE_CMD down
        ;;
    --update)
        echo "⬆️  拉取更新并重新构建..."
        git pull
        $COMPOSE_CMD up --build -d
        ;;
    *)
        echo "▶️ 启动服务..."
        $COMPOSE_CMD up -d
        ;;
esac

echo "✅ 完成！"
echo ""
echo "📍 Nuxt:   http://localhost"
echo "📍 API:    http://localhost/api"
echo "📍 Health: http://localhost/health"

#!/bin/bash
set -e

# PUBG Plus 部署脚本
# 用法:
#   ./scripts/deploy.sh             # 启动已有服务
#   ./scripts/deploy.sh --build     # 构建并启动
#   ./scripts/deploy.sh --update    # git pull + 重新构建
#   ./scripts/deploy.sh --prod      # 生产模式启动（DEV_MODE=false）
#   ./scripts/deploy.sh --stop      # 停止服务
#   ./scripts/deploy.sh --logs      # 查看日志
#   ./scripts/deploy.sh --shell     # 进入 API 容器 shell

echo "🚀 PUBG Plus Deploy"
echo "==================="

# 检查 .env
if [ ! -f .env ]; then
    echo "⚠️  请先创建 .env 文件（可参考 .env.example）"
    cat .env.example
    exit 1
fi

# 导出环境变量
set -a
source .env
set +a

COMPOSE_CMD="docker compose -f docker-compose.yml"

case "${1:-}" in
    --build|build)
        echo "🏗️  构建并启动..."
        $COMPOSE_CMD up --build -d
        ;;
    --prod|prod)
        echo "🏭 生产模式启动（DEV_MODE=false）..."
        export DEV_MODE=false
        $COMPOSE_CMD up --build -d
        ;;
    --update|update)
        echo "⬆️  拉取最新代码..."
        git pull
        echo "🏗️  重新构建..."
        $COMPOSE_CMD up --build -d
        ;;
    --restart|restart)
        echo "🔄 重启服务..."
        $COMPOSE_CMD restart
        ;;
    --logs|logs)
        echo "📋 查看日志（Ctrl+C 退出）..."
        $COMPOSE_CMD logs -f
        ;;
    --stop|stop)
        echo "🛑 停止服务（保留数据卷）..."
        $COMPOSE_CMD down
        ;;
    --down|down)
        echo "⚠️  停止服务并清理数据卷..."
        $COMPOSE_CMD down -v
        ;;
    --shell|shell)
        echo "🐚 进入 API 容器（输入 exit 退出）..."
        $COMPOSE_CMD exec api /bin/bash
        ;;
    --ps)
        echo "📊 容器状态："
        $COMPOSE_CMD ps
        ;;
    *)
        echo "▶️ 启动已有服务..."
        $COMPOSE_CMD up -d
        ;;
esac

echo ""
echo "✅ 完成！"
echo ""
echo "📍 Nuxt:   http://localhost:3000"
echo "📍 API:    http://localhost:8000"
echo "📍 Home:   http://localhost"
echo ""
echo "📖 更多命令:"
echo "   ./scripts/deploy.sh --build  构建并启动"
echo "   ./scripts/deploy.sh --prod   生产模式"
echo "   ./scripts/deploy.sh --logs   查看日志"
echo "   ./scripts/deploy.sh --shell  进入 API 容器"

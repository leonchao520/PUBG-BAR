# 构建阶段
FROM node:22-alpine AS builder

WORKDIR /app

# 复制依赖配置
COPY package.json package-lock.json ./

# 安装依赖（--frozen-lockfile 确保一致性）
RUN npm ci

# 复制源码
COPY . .

# 构建
RUN npm run build

# 运行阶段 - 更小的镜像
FROM node:22-alpine

WORKDIR /app

# 安装 curl 用于健康检查
RUN apk add --no-cache curl

# 从构建阶段复制产物
COPY --from=builder /app/.output ./.output

# 复制打包器包锁（用于关联构建）
COPY --from=builder /app/package.json /app/package-lock.json ./

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

CMD ["node", ".output/server/index.mjs"]

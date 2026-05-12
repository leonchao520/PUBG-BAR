// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-01-01",

  // SSR enabled for SEO
  ssr: true,

  // Route rules for ISR (Incremental Static Regeneration)
  routeRules: {
    // 首页 - 静态生成，每小时重新验证
    "/": { prerender: true },
    // 玩家搜索页 - 服务端渲染
    "/search": { ssr: true },
    // 玩家详情页 - ISR，30分钟重新验证
    "/player/**": { isr: 1800 },
    // 赛季排行 - ISR，1小时重新验证
    "/rankings/**": { isr: 3600 },
  },

  modules: ["@nuxtjs/tailwindcss"],

  // API 代理配置
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
    },
  },

  nitro: {
    // 开发时代理 API 请求
    devProxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },

  app: {
    head: {
      charset: "utf-8",
      viewport: "width=device-width, initial-scale=1",
      title: "PUBG Plus - 绝地求生数据工具",
      meta: [
        { name: "description", content: "查询 PUBG 玩家数据、战绩、赛季统计" },
        { name: "keywords", content: "PUBG, 绝地求生, 战绩查询, 数据统计" },
      ],
    },
  },
});

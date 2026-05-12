<script setup lang="ts">
import { ref } from "vue";

const route = useRoute();
const config = useRuntimeConfig();

const playerName = route.params.name as string;

// ISR 数据获取（在服务端执行）
const { data: player, pending, error } = await useFetch(
  `/api/players/${playerName}`,
  {
    baseURL: config.public.apiBase,
    server: true,       // SSR 时获取
    lazy: false,        // 等待数据再渲染
    key: `player-${playerName}`,   // 缓存 key
  }
);

// SEO meta（服务端生成）
useHead({
  title: `${playerName} PUBG 战绩查询 - PUBG Plus`,
  meta: [
    {
      name: "description",
      content: `查看 ${playerName} 的 PUBG 赛季数据、KD、胜率、比赛记录`,
    },
  ],
});
</script>

<template>
  <div>
    <!-- 加载状态 -->
    <div v-if="pending" class="flex justify-center py-20">
      <p class="text-gray-500">加载中...</p>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="text-center py-20">
      <p class="text-red-500">未找到玩家 "{{ playerName }}"</p>
      <NuxtLink to="/search" class="text-blue-500 hover:underline mt-4 inline-block">
        重新搜索
      </NuxtLink>
    </div>

    <!-- 玩家数据 -->
    <div v-else-if="player" class="space-y-6">
      <!-- 基本信息 -->
      <section class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center gap-4">
          <div class="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center text-2xl">
            {{ player.name?.charAt(0) || "?" }}
          </div>
          <div>
            <h1 class="text-2xl font-bold">{{ player.name }}</h1>
            <p class="text-gray-500 text-sm">等级 {{ player.level }} | 平台 {{ player.platform }}</p>
          </div>
        </div>
      </section>

      <!-- 赛季统计 -->
      <section class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">赛季统计</h2>
        <div v-if="player.season" class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="text-center p-3 bg-gray-50 rounded">
            <p class="text-2xl font-bold text-yellow-500">{{ player.season.kd?.toFixed(2) || "-" }}</p>
            <p class="text-sm text-gray-500">KD</p>
          </div>
          <div class="text-center p-3 bg-gray-50 rounded">
            <p class="text-2xl font-bold text-yellow-500">{{ player.season.winRate?.toFixed(1) || "-" }}%</p>
            <p class="text-sm text-gray-500">胜率</p>
          </div>
          <div class="text-center p-3 bg-gray-50 rounded">
            <p class="text-2xl font-bold text-yellow-500">{{ player.season.top10Rate?.toFixed(1) || "-" }}%</p>
            <p class="text-sm text-gray-500">前十率</p>
          </div>
          <div class="text-center p-3 bg-gray-50 rounded">
            <p class="text-2xl font-bold text-yellow-500">{{ player.season.games || "-" }}</p>
            <p class="text-sm text-gray-500">场次</p>
          </div>
        </div>
        <div v-else class="text-gray-400 text-center py-4">
          暂无赛季数据
        </div>
      </section>

      <!-- 最近比赛 -->
      <section class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">最近比赛</h2>
        <div v-if="player.recentMatches?.length" class="space-y-2">
          <div
            v-for="match in player.recentMatches"
            :key="match.id"
            class="flex items-center justify-between p-3 bg-gray-50 rounded hover:bg-gray-100 transition"
          >
            <div class="flex items-center gap-3">
              <span :class="match.win ? 'text-green-500' : 'text-red-400'">
                {{ match.win ? "🏆" : "💀" }}
              </span>
              <div>
                <p class="text-sm font-medium">{{ match.mode }}</p>
                <p class="text-xs text-gray-400">{{ match.time }}</p>
              </div>
            </div>
            <div class="text-right">
              <p class="text-sm font-bold">{{ match.kills }} 击杀</p>
              <p class="text-xs text-gray-400">{{ match.damage?.toFixed(0) }} 伤害</p>
            </div>
          </div>
        </div>
        <div v-else class="text-gray-400 text-center py-4">
          暂无比赛记录
        </div>
      </section>
    </div>
  </div>
</template>

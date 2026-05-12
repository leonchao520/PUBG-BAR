<script setup lang="ts">
import { ref } from "vue";
import type { AsyncData } from "nuxt/app";

interface PlayerData {
  id: string;
  name: string;
  platform: string;
  level: number;
  avatar_url: string | null;
  clan_name: string | null;
  season: {
    kd: number;
    winRate: number;
    top10Rate: number;
    games: number;
    avgDamage: number;
    bestRank: number;
    tier: string;
  } | null;
  recentMatches: Array<{
    id: string;
    mode: string;
    kills: number;
    damage: number;
    win: boolean;
    time: string;
  }>;
}

const route = useRoute();
const config = useRuntimeConfig();

const playerName = route.params.name as string;

const { data: player, pending, error } = await useFetch<{ data: PlayerData }>(
  `/api/players/${playerName}`,
  {
    baseURL: config.public.apiBase,
    server: true,
    lazy: false,
    key: `player-${playerName}`,
  }
);

useHead({
  title: computed(() => `${playerName} 战绩查询 - PUBG Plus`),
  meta: [
    {
      name: "description",
      content: computed(() => `查看 ${playerName} 的 PUBG 赛季数据、KD、胜率、比赛记录`),
    },
  ],
});

// 模式图标映射
const modeIcon: Record<string, string> = {
  solo: "1",
  duo: "2",
  squad: "4",
};
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-6 space-y-4">
    <!-- 加载状态 -->
    <div v-if="pending" class="flex flex-col items-center justify-center py-20">
      <div class="animate-spin w-10 h-10 border-2 border-pubg-accent border-t-transparent rounded-full mb-4"></div>
      <p class="text-pubg-muted text-sm uppercase tracking-wider">加载中...</p>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="text-center py-20">
      <p class="text-4xl mb-4">🔍</p>
      <p class="text-xl font-bold text-white mb-2">玩家未找到</p>
      <p class="text-pubg-muted text-sm mb-6">"{{ playerName }}" 不存在或输入有误</p>
      <NuxtLink
        to="/search"
        class="inline-block px-6 py-2.5 bg-pubg-accent text-pubg-dark font-bold rounded-md
               hover:bg-pubg-accent-hover transition-colors uppercase tracking-wider text-sm"
      >
        重新搜索
      </NuxtLink>
    </div>

    <!-- 玩家数据 -->
    <template v-else-if="player?.data">
      <!-- 头部信息 -->
      <div class="bg-pubg-card border border-pubg-border rounded-lg p-6">
        <div class="flex items-center gap-5">
          <!-- 头像 -->
          <div class="w-16 h-16 bg-pubg-border rounded-full flex items-center justify-center
                      text-2xl font-black text-pubg-accent border-2 border-pubg-accent/30 shrink-0">
            {{ player.data.name?.charAt(0)?.toUpperCase() }}
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-3 flex-wrap">
              <h1 class="text-2xl font-black text-white truncate">{{ player.data.name }}</h1>
              <span v-if="player.data.clan_name"
                    class="px-2 py-0.5 bg-pubg-accent/10 text-pubg-accent text-xs font-bold rounded uppercase tracking-wider">
                {{ player.data.clan_name }}
              </span>
            </div>
            <div class="flex items-center gap-3 text-xs text-pubg-muted mt-1">
              <span class="uppercase tracking-wider">{{ player.data.platform }}</span>
              <span class="text-pubg-border">|</span>
              <span>等级 {{ player.data.level }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 赛季数据面板 -->
      <div class="bg-pubg-card border border-pubg-border rounded-lg p-6">
        <h2 class="text-sm font-bold uppercase tracking-wider text-pubg-muted mb-4">
          赛季统计
        </h2>

        <div v-if="player.data.season" class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="bg-pubg-dark/50 border border-pubg-border rounded-lg p-4 text-center">
            <p class="text-3xl font-black text-pubg-accent">{{ player.data.season.kd?.toFixed(2) || "-" }}</p>
            <p class="text-xs text-pubg-muted uppercase tracking-wider mt-1">KD</p>
          </div>
          <div class="bg-pubg-dark/50 border border-pubg-border rounded-lg p-4 text-center">
            <p class="text-3xl font-black text-pubg-green">{{ player.data.season.winRate?.toFixed(1) || "-" }}%</p>
            <p class="text-xs text-pubg-muted uppercase tracking-wider mt-1">胜率</p>
          </div>
          <div class="bg-pubg-dark/50 border border-pubg-border rounded-lg p-4 text-center">
            <p class="text-3xl font-black text-white">{{ player.data.season.top10Rate?.toFixed(1) || "-" }}%</p>
            <p class="text-xs text-pubg-muted uppercase tracking-wider mt-1">前十率</p>
          </div>
          <div class="bg-pubg-dark/50 border border-pubg-border rounded-lg p-4 text-center">
            <p class="text-3xl font-black text-white">{{ player.data.season.games || "-" }}</p>
            <p class="text-xs text-pubg-muted uppercase tracking-wider mt-1">场次</p>
          </div>
        </div>

        <!-- 无数据 -->
        <div v-else class="text-center py-8 text-pubg-muted/60">
          <p class="text-sm">暂无赛季数据</p>
          <p class="text-xs mt-1">数据将在查询后自动生成</p>
        </div>
      </div>

      <!-- 比赛记录 -->
      <div class="bg-pubg-card border border-pubg-border rounded-lg p-6">
        <h2 class="text-sm font-bold uppercase tracking-wider text-pubg-muted mb-4">
          最近比赛
        </h2>

        <div v-if="player.data.recentMatches?.length" class="space-y-2">
          <div
            v-for="(match, i) in player.data.recentMatches"
            :key="match.id"
            class="flex items-center gap-3 px-4 py-3 bg-pubg-dark/30 border border-pubg-border rounded-lg
                   hover:bg-pubg-card-hover transition-colors group"
          >
            <!-- 吃鸡标志 -->
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-sm shrink-0"
                 :class="match.win ? 'bg-pubg-green/20 text-pubg-green' : 'bg-pubg-red/20 text-pubg-red'">
              {{ match.win ? '🏆' : '💀' }}
            </div>

            <!-- 模式 + 时间 -->
            <div class="flex-1 min-w-0">
              <p class="text-sm font-bold text-white">
                {{ match.mode }}
              </p>
              <p class="text-xs text-pubg-muted/60">{{ match.time ? new Date(match.time).toLocaleDateString() : '-' }}</p>
            </div>

            <!-- 数据 -->
            <div class="flex items-center gap-4 text-right">
              <div>
                <p class="text-sm font-bold text-pubg-accent">{{ match.kills }}</p>
                <p class="text-xs text-pubg-muted uppercase tracking-wider">击杀</p>
              </div>
              <div>
                <p class="text-sm font-bold text-white">{{ match.damage?.toFixed(0) || '-' }}</p>
                <p class="text-xs text-pubg-muted uppercase tracking-wider">伤害</p>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-8 text-pubg-muted/60">
          <p class="text-sm">暂无比赛记录</p>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
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
    winPlace?: number;
    assists?: number;
    duration?: number;
  }>;
}

const route = useRoute();
const config = useRuntimeConfig();
const activeTab = ref<"overview" | "matches">("overview");

const playerName = route.params.name as string;

// Fetch player data from unified endpoint (includes season + matches)
const { data: player, pending, error } = await useFetch<{ data: PlayerData }>(
  `/api/players/${playerName}`,
  {
    baseURL: config.public.apiBase,
    server: true,
    lazy: false,
    key: `player-${playerName}`,
  }
);

// Also fetch separate season and matches for fallback/detail
const {
  data: seasonData,
  pending: seasonPending,
} = await useFetch<{ data: PlayerData["season"] }>(
  `/api/players/${playerName}/season`,
  {
    baseURL: config.public.apiBase,
    server: false,
    lazy: true,
    key: `player-season-${playerName}`,
  }
);

const {
  data: matchesData,
  pending: matchesPending,
} = await useFetch<{ data: PlayerData["recentMatches"] }>(
  `/api/players/${playerName}/matches`,
  {
    baseURL: config.public.apiBase,
    server: false,
    lazy: true,
    key: `player-matches-${playerName}`,
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

// Resolved season & matches (main data first, fallback to detail endpoint)
const resolvedSeason = computed(() => {
  return player.value?.data?.season || seasonData.value?.data || null;
});

const resolvedMatches = computed(() => {
  return player.value?.data?.recentMatches || matchesData.value?.data || [];
});

function formatDuration(seconds: number): string {
  const min = Math.floor(seconds / 60);
  const sec = seconds % 60;
  return `${min}:${sec.toString().padStart(2, "0")}`;
}
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
              <span v-if="resolvedSeason?.tier"
                    class="px-2 py-0.5 bg-pubg-green/10 text-pubg-green text-xs font-bold rounded uppercase tracking-wider">
                {{ resolvedSeason.tier }}
              </span>
            </div>
            <div class="flex items-center gap-3 text-xs text-pubg-muted mt-1">
              <span class="uppercase tracking-wider">{{ player.data.platform }}</span>
              <span class="text-pubg-border">|</span>
              <span>等级 {{ player.data.level }}</span>
              <span class="text-pubg-border">|</span>
              <span>{{ resolvedSeason?.games || 0 }} 场</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab 切换 -->
      <div class="flex gap-1 bg-pubg-card border border-pubg-border rounded-lg p-1">
        <button
          @click="activeTab = 'overview'"
          class="flex-1 py-2.5 text-sm font-bold uppercase tracking-wider rounded-md transition-all"
          :class="activeTab === 'overview'
            ? 'bg-pubg-accent text-pubg-dark shadow-lg'
            : 'text-pubg-muted hover:text-white hover:bg-pubg-border'"
        >
          赛季概览
        </button>
        <button
          @click="activeTab = 'matches'"
          class="flex-1 py-2.5 text-sm font-bold uppercase tracking-wider rounded-md transition-all"
          :class="activeTab === 'matches'
            ? 'bg-pubg-accent text-pubg-dark shadow-lg'
            : 'text-pubg-muted hover:text-white hover:bg-pubg-border'"
        >
          比赛记录
        </button>
      </div>

      <!-- 赛季概览 Tab -->
      <div v-if="activeTab === 'overview'" class="space-y-4">
        <div class="bg-pubg-card border border-pubg-border rounded-lg p-6">
          <h2 class="text-sm font-bold uppercase tracking-wider text-pubg-muted mb-4">
            核心数据
          </h2>

          <div v-if="resolvedSeason" class="space-y-4">
            <!-- KPI 卡片 -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div class="bg-pubg-dark/50 border border-pubg-border rounded-lg p-4 text-center">
                <p class="text-3xl font-black text-pubg-accent">{{ resolvedSeason.kd?.toFixed(2) }}</p>
                <p class="text-xs text-pubg-muted uppercase tracking-wider mt-1">KD</p>
              </div>
              <div class="bg-pubg-dark/50 border border-pubg-border rounded-lg p-4 text-center">
                <p class="text-3xl font-black text-pubg-green">{{ resolvedSeason.winRate?.toFixed(1) }}%</p>
                <p class="text-xs text-pubg-muted uppercase tracking-wider mt-1">胜率</p>
              </div>
              <div class="bg-pubg-dark/50 border border-pubg-border rounded-lg p-4 text-center">
                <p class="text-3xl font-black text-white">{{ resolvedSeason.top10Rate?.toFixed(1) }}%</p>
                <p class="text-xs text-pubg-muted uppercase tracking-wider mt-1">前十率</p>
              </div>
              <div class="bg-pubg-dark/50 border border-pubg-border rounded-lg p-4 text-center">
                <p class="text-3xl font-black text-white">{{ resolvedSeason.avgDamage?.toFixed(0) }}</p>
                <p class="text-xs text-pubg-muted uppercase tracking-wider mt-1">场均伤害</p>
              </div>
            </div>

            <!-- 进阶数据 -->
            <div class="border-t border-pubg-border pt-4">
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <div class="flex items-center justify-between px-4 py-3 bg-pubg-dark/30 border border-pubg-border rounded-lg">
                  <span class="text-xs text-pubg-muted uppercase tracking-wider">总场次</span>
                  <span class="text-sm font-bold text-white">{{ resolvedSeason.games }}</span>
                </div>
                <div class="flex items-center justify-between px-4 py-3 bg-pubg-dark/30 border border-pubg-border rounded-lg">
                  <span class="text-xs text-pubg-muted uppercase tracking-wider">最佳排名</span>
                  <span class="text-sm font-bold text-white">#{{ resolvedSeason.bestRank }}</span>
                </div>
                <div class="flex items-center justify-between px-4 py-3 bg-pubg-dark/30 border border-pubg-border rounded-lg">
                  <span class="text-xs text-pubg-muted uppercase tracking-wider">段位</span>
                  <span class="text-sm font-bold text-pubg-accent">{{ resolvedSeason.tier }}</span>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-8 text-pubg-muted/60">
            <div v-if="seasonPending" class="flex items-center justify-center gap-2">
              <div class="animate-spin w-4 h-4 border-2 border-pubg-accent border-t-transparent rounded-full"></div>
              <span class="text-sm">加载赛季数据...</span>
            </div>
            <p v-else class="text-sm">暂无赛季数据</p>
          </div>
        </div>
      </div>

      <!-- 比赛记录 Tab -->
      <div v-if="activeTab === 'matches'">
        <div class="bg-pubg-card border border-pubg-border rounded-lg p-6">
          <h2 class="text-sm font-bold uppercase tracking-wider text-pubg-muted mb-4">
            最近比赛
            <span v-if="resolvedMatches.length" class="ml-2 text-pubg-accent">({{ resolvedMatches.length }})</span>
          </h2>

          <!-- 比赛概览统计 -->
          <div v-if="resolvedMatches.length" class="grid grid-cols-3 gap-3 mb-4">
            <div class="bg-pubg-dark/30 border border-pubg-border rounded-lg p-3 text-center">
              <p class="text-lg font-black text-white">{{ resolvedMatches.filter(m => m.win).length }}</p>
              <p class="text-xs text-pubg-muted uppercase tracking-wider">吃鸡</p>
            </div>
            <div class="bg-pubg-dark/30 border border-pubg-border rounded-lg p-3 text-center">
              <p class="text-lg font-black text-pubg-accent">{{ resolvedMatches.reduce((s, m) => s + m.kills, 0) }}</p>
              <p class="text-xs text-pubg-muted uppercase tracking-wider">总击杀</p>
            </div>
            <div class="bg-pubg-dark/30 border border-pubg-border rounded-lg p-3 text-center">
              <p class="text-lg font-black text-white">{{ (resolvedMatches.reduce((s, m) => s + m.damage, 0) / resolvedMatches.length).toFixed(0) }}</p>
              <p class="text-xs text-pubg-muted uppercase tracking-wider">场均伤害</p>
            </div>
          </div>

          <!-- 比赛列表 -->
          <div v-if="resolvedMatches.length" class="space-y-2">
            <div
              v-for="match in resolvedMatches"
              :key="match.id"
              class="flex items-center gap-3 px-4 py-3 bg-pubg-dark/30 border border-pubg-border rounded-lg
                     hover:bg-pubg-card-hover transition-colors group"
            >
              <!-- 吃鸡标志 + 排名 -->
              <div class="flex flex-col items-center gap-0.5 w-10 shrink-0">
                <div class="w-8 h-8 rounded-full flex items-center justify-center text-sm"
                     :class="match.win ? 'bg-pubg-green/20' : 'bg-pubg-red/20'">
                  <span v-if="match.win" class="text-pubg-green">🏆</span>
                  <span v-else-if="match.winPlace && match.winPlace <= 10" class="text-pubg-blue text-xs font-bold">#{{ match.winPlace }}</span>
                  <span v-else class="text-pubg-red text-xs font-bold">💀</span>
                </div>
              </div>

              <!-- 模式 + 时间 -->
              <div class="flex-1 min-w-0">
                <p class="text-sm font-bold text-white capitalize">
                  {{ match.mode?.replace("-", " ") }}
                </p>
                <p class="text-xs text-pubg-muted/60">
                  {{ match.time ? new Date(match.time).toLocaleDateString("zh-CN", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }) : "-" }}
                </p>
              </div>

              <!-- K/D 数据 -->
              <div class="flex items-center gap-4 text-right">
                <div>
                  <p class="text-sm font-bold text-pubg-accent">{{ match.kills }}</p>
                  <p class="text-xs text-pubg-muted uppercase tracking-wider">击杀</p>
                </div>
                <div>
                  <p class="text-sm font-bold text-white">{{ match.damage?.toFixed(0) }}</p>
                  <p class="text-xs text-pubg-muted uppercase tracking-wider">伤害</p>
                </div>
                <div v-if="match.assists !== undefined" class="hidden md:block">
                  <p class="text-sm font-bold text-pubg-muted">{{ match.assists }}</p>
                  <p class="text-xs text-pubg-muted uppercase tracking-wider">助攻</p>
                </div>
                <div v-if="match.duration" class="hidden md:block">
                  <p class="text-sm font-bold text-white">{{ formatDuration(match.duration) }}</p>
                  <p class="text-xs text-pubg-muted uppercase tracking-wider">时长</p>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-8 text-pubg-muted/60">
            <div v-if="matchesPending" class="flex items-center justify-center gap-2">
              <div class="animate-spin w-4 h-4 border-2 border-pubg-accent border-t-transparent rounded-full"></div>
              <span class="text-sm">加载比赛记录...</span>
            </div>
            <p v-else class="text-sm">暂无比赛记录</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.text-pubg-blue {
  color: #63b3ed;
}
</style>

<script setup lang="ts">
import { ref } from "vue";

interface RankingItem {
  rank: number;
  name: string;
  level: number;
  kd: number;
  winRate: number;
  tier: string;
  games: number;
}

const config = useRuntimeConfig();
const currentPage = ref(1);
const pageSize = 20;

const { data: rankings, pending } = await useFetch<{ data: { items: RankingItem[]; total: number } }>(
  `/api/rankings?page=${currentPage.value}&page_size=${pageSize}`,
  {
    baseURL: config.public.apiBase,
    server: true,
    lazy: false,
    key: "rankings",
  }
);

// Tier color mapping
const tierColors: Record<string, string> = {
  Conqueror: "text-red-400",
  Master: "text-purple-400",
  Diamond: "text-blue-400",
  Platinum: "text-cyan-400",
  Gold: "text-yellow-400",
  Silver: "text-gray-400",
  Bronze: "text-orange-400",
};

useHead({
  title: "排行榜 - PUBG Plus",
  meta: [
    { name: "description", content: "查看 PUBG 赛季排行榜、玩家 KD、胜率、段位排名" },
  ],
});
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-black uppercase tracking-wider">排行榜</h1>
        <p class="text-pubg-muted text-xs mt-1 uppercase tracking-wider">
          赛季综合排名 · {{ rankings?.data?.total || 0 }} 名玩家
        </p>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="pending" class="flex flex-col items-center justify-center py-20">
      <div class="animate-spin w-10 h-10 border-2 border-pubg-accent border-t-transparent rounded-full mb-4"></div>
      <p class="text-pubg-muted text-sm uppercase tracking-wider">加载中...</p>
    </div>

    <!-- 无数据 -->
    <div v-else-if="!rankings?.data?.items?.length" class="bg-pubg-card border border-pubg-border rounded-lg p-12 text-center">
      <div class="text-5xl mb-4">🏗️</div>
      <p class="text-pubg-muted text-lg font-bold mb-2">数据生成中</p>
      <p class="text-xs text-pubg-muted/60 max-w-xs mx-auto">
        排行榜数据将在玩家数据积累后自动生成
      </p>
    </div>

    <!-- 排行榜表格 -->
    <div v-else class="bg-pubg-card border border-pubg-border rounded-lg overflow-hidden">
      <!-- 表头 -->
      <div class="grid grid-cols-12 gap-2 px-4 py-3 border-b border-pubg-border bg-pubg-dark/30">
        <span class="col-span-1 text-xs text-pubg-muted font-bold uppercase tracking-wider text-center">#</span>
        <span class="col-span-4 text-xs text-pubg-muted font-bold uppercase tracking-wider">玩家</span>
        <span class="col-span-2 text-xs text-pubg-muted font-bold uppercase tracking-wider text-right">KD</span>
        <span class="col-span-2 text-xs text-pubg-muted font-bold uppercase tracking-wider text-right">胜率</span>
        <span class="col-span-1 text-xs text-pubg-muted font-bold uppercase tracking-wider text-center">段位</span>
        <span class="col-span-2 text-xs text-pubg-muted font-bold uppercase tracking-wider text-right">场次</span>
      </div>

      <!-- 行 -->
      <NuxtLink
        v-for="item in rankings?.data?.items"
        :key="item.rank"
        :to="`/player/${item.name}`"
        class="grid grid-cols-12 gap-2 px-4 py-3.5 border-b border-pubg-border last:border-b-0
               hover:bg-pubg-card-hover transition-colors items-center group"
      >
        <!-- 排名 -->
        <div class="col-span-1 flex justify-center">
          <span v-if="item.rank === 1" class="text-lg">🥇</span>
          <span v-else-if="item.rank === 2" class="text-lg">🥈</span>
          <span v-else-if="item.rank === 3" class="text-lg">🥉</span>
          <span v-else class="text-sm font-bold text-pubg-muted group-hover:text-white transition-colors">
            {{ item.rank }}
          </span>
        </div>

        <!-- 玩家名 -->
        <div class="col-span-4 flex items-center gap-3 min-w-0">
          <div class="w-8 h-8 bg-pubg-border rounded-full flex items-center justify-center
                      text-xs font-bold text-pubg-accent uppercase shrink-0">
            {{ item.name?.charAt(0) }}
          </div>
          <span class="font-bold text-white truncate group-hover:text-pubg-accent transition-colors text-sm">
            {{ item.name }}
          </span>
        </div>

        <!-- KD -->
        <div class="col-span-2 text-right">
          <span class="text-sm font-bold text-pubg-accent">{{ item.kd?.toFixed(2) }}</span>
        </div>

        <!-- 胜率 -->
        <div class="col-span-2 text-right">
          <span class="text-sm font-bold text-pubg-green">{{ item.winRate?.toFixed(1) }}%</span>
        </div>

        <!-- 段位 -->
        <div class="col-span-1 text-center">
          <span class="text-xs font-bold uppercase tracking-wider" :class="tierColors[item.tier] || 'text-pubg-muted'">
            {{ item.tier?.substring(0, 3) || "-" }}
          </span>
        </div>

        <!-- 场次 -->
        <div class="col-span-2 text-right">
          <span class="text-sm text-pubg-muted">{{ item.games }}</span>
        </div>
      </NuxtLink>
    </div>

    <!-- 底部说明 -->
    <div class="mt-4 text-center">
      <p class="text-xs text-pubg-muted/60">
        数据基于赛季综合表现排名 · 实时更新
      </p>
    </div>
  </div>
</template>

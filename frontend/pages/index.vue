<script setup lang="ts">
import { ref } from "vue";

const searchQuery = ref("");
const isSearching = ref(false);

async function handleSearch() {
  if (!searchQuery.value.trim()) return;
  isSearching.value = true;
  await navigateTo(`/player/${searchQuery.value.trim()}`);
}

// SEO
useHead({
  title: "PUBG Plus - 绝地求生数据查询工具",
  meta: [
    { name: "description", content: "查询 PUBG 玩家战绩、KD、胜率、赛季数据、比赛记录 — PUBG Plus 非官方数据工具" },
  ],
});
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-[80vh] px-4">
    <!-- Hero -->
    <div class="text-center mb-10">
      <h1 class="text-5xl md:text-7xl font-black tracking-widest uppercase mb-3">
        <span class="text-pubg-accent">PUBG</span>
        <span class="text-white/90"> Plus</span>
      </h1>
      <p class="text-pubg-muted text-sm md:text-base tracking-wider uppercase">
        PUBG 玩家数据 · 实时查询
      </p>
    </div>

    <!-- 搜索框 -->
    <form @submit.prevent="handleSearch" class="w-full max-w-xl">
      <div class="relative group">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="输入玩家昵称..."
          class="w-full px-5 py-4 pr-28 bg-pubg-card border border-pubg-border rounded-lg
                 text-white placeholder-pubg-muted/50
                 focus:outline-none focus:border-pubg-accent focus:ring-1 focus:ring-pubg-accent/50
                 transition-all text-lg"
        />
        <button
          type="submit"
          :disabled="isSearching"
          class="absolute right-1.5 top-1/2 -translate-y-1/2 px-6 py-2.5
                 bg-pubg-accent text-pubg-dark font-bold rounded-md
                 hover:bg-pubg-accent-hover transition-colors
                 disabled:opacity-50 uppercase tracking-wider text-sm"
        >
          {{ isSearching ? "..." : "查询" }}
        </button>
      </div>
    </form>

    <!-- 功能卡片 -->
    <section class="mt-16 grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-3xl">
      <div class="bg-pubg-card border border-pubg-border rounded-lg p-5 text-center hover:border-pubg-accent/30 transition-colors">
        <div class="text-2xl mb-2">📊</div>
        <h3 class="font-bold text-white uppercase tracking-wider text-sm mb-1">赛季数据</h3>
        <p class="text-xs text-pubg-muted">KD / 胜率 / 场均伤害 / 排名</p>
      </div>
      <div class="bg-pubg-card border border-pubg-border rounded-lg p-5 text-center hover:border-pubg-accent/30 transition-colors">
        <div class="text-2xl mb-2">🎯</div>
        <h3 class="font-bold text-white uppercase tracking-wider text-sm mb-1">比赛记录</h3>
        <p class="text-xs text-pubg-muted">最近对局 · 击杀详情 · 表现分析</p>
      </div>
      <div class="bg-pubg-card border border-pubg-border rounded-lg p-5 text-center hover:border-pubg-accent/30 transition-colors">
        <div class="text-2xl mb-2">🏆</div>
        <h3 class="font-bold text-white uppercase tracking-wider text-sm mb-1">排行榜</h3>
        <p class="text-xs text-pubg-muted">综合排名 · 段位分布 · 趋势</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const query = ref("");
const results = ref<any[]>([]);
const isSearching = ref(false);
const searched = ref(false);

useHead({
  title: "玩家查询 - PUBG Plus",
});

async function search() {
  if (!query.value.trim()) return;
  isSearching.value = true;
  searched.value = true;

  try {
    const config = useRuntimeConfig();
    const res: any = await $fetch(`/api/players/search?q=${encodeURIComponent(query.value)}`, {
      baseURL: config.public.apiBase,
    });
    results.value = res?.data || [];
  } catch {
    results.value = [];
  } finally {
    isSearching.value = false;
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-black uppercase tracking-wider mb-6">玩家查询</h1>

    <!-- 搜索框 -->
    <form @submit.prevent="search" class="relative mb-8">
      <div class="relative group">
        <input
          v-model="query"
          type="text"
          placeholder="输入玩家昵称..."
          class="w-full px-5 py-3.5 pr-24 bg-pubg-card border border-pubg-border rounded-lg
                 text-white placeholder-pubg-muted/50
                 focus:outline-none focus:border-pubg-accent focus:ring-1 focus:ring-pubg-accent/50
                 transition-all"
        />
        <button
          type="submit"
          :disabled="isSearching"
          class="absolute right-1.5 top-1/2 -translate-y-1/2 px-5 py-2
                 bg-pubg-accent text-pubg-dark font-bold rounded-md
                 hover:bg-pubg-accent-hover transition-colors
                 disabled:opacity-50 uppercase tracking-wider text-sm"
        >
          {{ isSearching ? "..." : "搜索" }}
        </button>
      </div>
    </form>

    <!-- 加载状态 -->
    <div v-if="isSearching" class="text-center py-12">
      <div class="animate-spin w-8 h-8 border-2 border-pubg-accent border-t-transparent rounded-full mx-auto mb-3"></div>
      <p class="text-pubg-muted text-sm">搜索中...</p>
    </div>

    <!-- 无结果 -->
    <div v-else-if="searched && !results.length" class="text-center py-12">
      <p class="text-pubg-muted">未找到匹配的玩家</p>
      <p class="text-xs text-pubg-muted/60 mt-2">请检查昵称是否正确</p>
    </div>

    <!-- 结果列表 -->
    <div v-else-if="results.length" class="space-y-2">
      <NuxtLink
        v-for="player in results"
        :key="player.id"
        :to="`/player/${player.name}`"
        class="flex items-center gap-4 p-4 bg-pubg-card border border-pubg-border rounded-lg
               hover:bg-pubg-card-hover hover:border-pubg-accent/30 transition-all group"
      >
        <div class="w-10 h-10 bg-pubg-border rounded-full flex items-center justify-center
                    text-sm font-bold text-pubg-accent uppercase group-hover:bg-pubg-accent/20 transition-colors">
          {{ player.name?.charAt(0) }}
        </div>
        <div class="flex-1">
          <p class="font-bold text-white group-hover:text-pubg-accent transition-colors">{{ player.name }}</p>
          <p class="text-xs text-pubg-muted uppercase tracking-wider">{{ player.platform }}</p>
        </div>
        <svg class="w-4 h-4 text-pubg-muted group-hover:text-pubg-accent transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </NuxtLink>
    </div>
  </div>
</template>

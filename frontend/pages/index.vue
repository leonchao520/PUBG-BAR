<script setup lang="ts">
import { ref } from "vue";

const searchQuery = ref("");
const isSearching = ref(false);

async function handleSearch() {
  if (!searchQuery.value.trim()) return;
  isSearching.value = true;
  // 页面跳转交给 Nuxt 路由
  await navigateTo(`/player/${searchQuery.value.trim()}`);
}
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-[70vh]">
    <h1 class="text-4xl font-bold mb-4">PUBG Plus</h1>
    <p class="text-gray-600 mb-8">查询 PUBG 玩家战绩、赛季数据、比赛记录</p>

    <form @submit.prevent="handleSearch" class="w-full max-w-md">
      <div class="flex gap-2">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="输入玩家昵称..."
          class="flex-1 px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400"
        />
        <button
          type="submit"
          :disabled="isSearching"
          class="px-6 py-3 bg-yellow-400 text-black font-bold rounded-lg hover:bg-yellow-300 disabled:opacity-50"
        >
          {{ isSearching ? "搜索中..." : "查询" }}
        </button>
      </div>
    </form>

    <!-- SEO 友好内容 -->
    <section class="mt-16 text-center text-gray-500 max-w-2xl">
      <h2 class="text-xl font-semibold text-gray-700 mb-4">功能介绍</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="p-4">
          <h3 class="font-bold text-gray-800 mb-2">玩家数据</h3>
          <p class="text-sm">查询 KD、胜率、场均伤害等核心数据</p>
        </div>
        <div class="p-4">
          <h3 class="font-bold text-gray-800 mb-2">赛季统计</h3>
          <p class="text-sm">查看各赛季排名、段位变化趋势</p>
        </div>
        <div class="p-4">
          <h3 class="font-bold text-gray-800 mb-2">比赛记录</h3>
          <p class="text-sm">回顾最近比赛详情，每局数据全掌握</p>
        </div>
      </div>
    </section>
  </div>
</template>

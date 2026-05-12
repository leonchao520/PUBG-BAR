<script setup lang="ts">
import { ref } from "vue";

const query = ref("");
const results = ref<any[]>([]);
const isSearching = ref(false);
const searched = ref(false);

useHead({
  title: "PUBG 玩家查询 - PUBG Plus",
});

async function search() {
  if (!query.value.trim()) return;
  isSearching.value = true;
  searched.value = true;

  try {
    const config = useRuntimeConfig();
    const { data } = await $fetch(`/api/players/search?q=${encodeURIComponent(query.value)}`, {
      baseURL: config.public.apiBase,
    });
    results.value = data || [];
  } catch {
    results.value = [];
  } finally {
    isSearching.value = false;
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto">
    <h1 class="text-2xl font-bold mb-6">玩家查询</h1>

    <form @submit.prevent="search" class="flex gap-2 mb-8">
      <input
        v-model="query"
        type="text"
        placeholder="输入玩家昵称..."
        class="flex-1 px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400"
      />
      <button
        type="submit"
        :disabled="isSearching"
        class="px-6 py-3 bg-yellow-400 text-black font-bold rounded-lg hover:bg-yellow-300 disabled:opacity-50"
      >
        {{ isSearching ? "搜索中..." : "搜索" }}
      </button>
    </form>

    <div v-if="isSearching" class="text-center text-gray-500 py-8">
      搜索中...
    </div>

    <div v-else-if="searched && !results.length" class="text-center text-gray-500 py-8">
      未找到匹配的玩家
    </div>

    <div v-else-if="results.length" class="space-y-3">
      <NuxtLink
        v-for="player in results"
        :key="player.id"
        :to="`/player/${player.name}`"
        class="block p-4 bg-white rounded-lg shadow hover:shadow-md transition"
      >
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
            {{ player.name?.charAt(0) }}
          </div>
          <div>
            <p class="font-bold">{{ player.name }}</p>
            <p class="text-sm text-gray-500">{{ player.platform }}</p>
          </div>
        </div>
      </NuxtLink>
    </div>
  </div>
</template>

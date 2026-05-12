<template>
  <div>
    <header class="bg-gray-900 text-white p-4">
      <div class="container mx-auto flex items-center justify-between">
        <NuxtLink to="/" class="text-xl font-bold">PUBG Plus 🦐</NuxtLink>
        <nav class="flex gap-4">
          <NuxtLink to="/search" class="hover:text-yellow-400">玩家查询</NuxtLink>
          <NuxtLink to="/rankings" class="hover:text-yellow-400">排行榜</NuxtLink>
        </nav>
      </div>
    </header>
    <main class="container mx-auto p-4">
      <NuxtPage />
    </main>
    <footer class="bg-gray-900 text-white text-center p-4 text-sm text-gray-400">
      PUBG Plus - 非官方数据工具 | Powered by PUBG API
    </footer>
  </div>
</template>

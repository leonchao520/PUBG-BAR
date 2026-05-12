<template>
  <div class="min-h-screen bg-pubg-dark flex flex-col">
    <!-- 顶栏 -->
    <header class="border-b border-pubg-border bg-pubg-card/80 backdrop-blur-sm sticky top-0 z-50">
      <div class="container mx-auto px-4 h-14 flex items-center justify-between">
        <NuxtLink to="/" class="flex items-center gap-2 font-black text-lg tracking-wider uppercase">
          <span class="text-pubg-accent">PUBG</span>
          <span class="text-white/80">Plus</span>
        </NuxtLink>
        <nav class="flex items-center gap-1">
          <NuxtLink
            to="/search"
            class="px-3 py-1.5 text-sm text-pubg-muted hover:text-white hover:bg-pubg-border rounded transition-colors"
          >
            查询
          </NuxtLink>
          <NuxtLink
            to="/rankings"
            class="px-3 py-1.5 text-sm text-pubg-muted hover:text-white hover:bg-pubg-border rounded transition-colors"
          >
            排行
          </NuxtLink>
        </nav>
      </div>
    </header>

    <!-- 主体 -->
    <main class="flex-1">
      <NuxtPage />
    </main>

    <!-- 底栏 -->
    <footer class="border-t border-pubg-border bg-pubg-card/50 py-4 mt-auto">
      <div class="container mx-auto px-4 text-center">
        <p class="text-xs text-pubg-muted/60 tracking-wider uppercase">
          PUBG Plus · 非官方数据工具 · Powered by PUBG API
        </p>
      </div>
    </footer>
  </div>
</template>

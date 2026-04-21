<template>
  <el-config-provider :locale="zhCn">
    <AppHeader v-if="!isAuthPage" />
    <main class="main-content" :class="{ 'no-header': isAuthPage }">
      <RouterView />
    </main>
    <AppFooter v-if="!isAuthPage" />
  </el-config-provider>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import AppHeader from '@/components/common/AppHeader.vue'
import AppFooter from '@/components/common/AppFooter.vue'

const route = useRoute()
const isAuthPage = computed(() => ['/login', '/register'].includes(route.path))
</script>

<template>
  <div class="app-loading" v-if="show">
    <el-icon class="is-loading"><Loading /></el-icon>
    <p>{{ text || '加载中...' }}</p>
  </div>
</template>

<script setup>
import { Loading } from '@element-plus/icons-vue'

defineProps({
  show: { type: Boolean, default: true },
  text: { type: String, default: '' }
})
</script>

<style scoped>
.app-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #999;
}
.app-loading .el-icon {
  font-size: 32px;
  margin-bottom: 12px;
}
</style>

<template>
  <el-avatar :src="getImageUrl(src)" :size="size" :shape="shape">
    <el-icon><User /></el-icon>
  </el-avatar>
</template>

<script setup>
import { User } from '@element-plus/icons-vue'

const props = defineProps({
  src: { type: String, default: '' },
  size: { type: [Number, String], default: 40 },
  shape: { type: String, default: 'circle' }
})

function getImageUrl(path) {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `http://localhost:5000${path}`
}
</script>

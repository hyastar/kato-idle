<template>
  <div class="item-card" @click="goToDetail">
    <div class="card-image">
      <el-image :src="getImageUrl(item.cover)" fit="cover" lazy>
        <template #error>
          <div class="image-error">📦</div>
        </template>
      </el-image>
      <div class="condition-badge">{{ item.condition_text }}</div>
      <div class="status-badge sold" v-if="item.status === 2">已售出</div>
    </div>
    <div class="card-info">
      <p class="item-title">{{ item.title }}</p>
      <div class="item-footer">
        <span class="item-price">¥{{ item.price }}</span>
        <span class="item-views">👁 {{ item.view_count }}</span>
      </div>
      <p class="item-time">{{ formatTime(item.created_at) }}</p>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  item: { type: Object, required: true }
})

const router = useRouter()

function goToDetail() {
  router.push(`/item/${props.item.id}`)
}

function getImageUrl(path) {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `http://localhost:5000${path}`
}

function formatTime(timeStr) {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / 86400000)
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 30) return `${days}天前`
  return timeStr.split(' ')[0]
}
</script>

<style scoped>
.item-card {
  border-radius: 10px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.item-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}
.card-image {
  position: relative;
  height: 180px;
  overflow: hidden;
  background: #f5f5f5;
}
.card-image .el-image {
  width: 100%;
  height: 100%;
}
.image-error {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  font-size: 40px;
}
.condition-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  background: rgba(0,0,0,0.5);
  color: white;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 4px;
}
.status-badge.sold {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: rgba(0,0,0,0.5);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
}
.card-info {
  padding: 10px 12px;
}
.item-title {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.item-price {
  font-size: 18px;
  font-weight: bold;
  color: #f56c6c;
}
.item-views {
  font-size: 12px;
  color: #999;
}
.item-time {
  font-size: 11px;
  color: #ccc;
  margin-top: 4px;
}
</style>

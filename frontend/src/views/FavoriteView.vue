<template>
  <div class="container page-padding">
    <h2 class="page-title">我的收藏</h2>

    <el-skeleton :loading="loading" animated>
      <template #default>
        <div class="items-grid" v-if="items.length">
          <div v-for="fav in items" :key="fav.id" class="item-wrap">
            <ItemCard v-if="fav.item" :item="fav.item" />
            <el-button size="small" type="danger" @click="handleRemove(fav.item_id)">取消收藏</el-button>
          </div>
        </div>
        <el-empty v-else description="暂无收藏物品" />
      </template>
    </el-skeleton>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getFavorites, removeFavorite } from '@/api/favorite'
import ItemCard from '@/components/item/ItemCard.vue'

const loading = ref(false)
const items = ref([])

async function fetchFavorites() {
  loading.value = true
  try {
    const res = await getFavorites()
    items.value = res.data
  } finally {
    loading.value = false
  }
}

async function handleRemove(itemId) {
  try {
    await removeFavorite(itemId)
    ElMessage.success('已取消收藏')
    fetchFavorites()
  } catch {}
}

onMounted(fetchFavorites)
</script>

<style scoped>
.page-title { margin-bottom: 20px; }
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
.item-wrap { display: flex; flex-direction: column; gap: 8px; }
</style>

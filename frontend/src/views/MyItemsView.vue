<template>
  <div class="container page-padding">
    <h2 class="page-title">我发布的物品</h2>

    <div class="filter-row">
      <el-select v-model="filters.status" @change="fetchItems" placeholder="状态筛选" style="width:150px" clearable>
        <el-option label="全部" :value="undefined" />
        <el-option label="在售" :value="1" />
        <el-option label="已售" :value="2" />
        <el-option label="已下架" :value="0" />
      </el-select>
    </div>

    <el-skeleton :loading="loading" animated>
      <template #default>
        <div class="items-grid" v-if="items.length">
          <div v-for="item in items" :key="item.id" class="item-wrap">
            <ItemCard :item="item" />
            <div class="item-actions">
              <el-button size="small" @click="router.push(`/publish?edit=${item.id}`)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(item.id)">删除</el-button>
            </div>
          </div>
        </div>
        <el-empty v-else description="暂无发布的物品" />
      </template>
    </el-skeleton>

    <div class="pagination-wrap" v-if="total > filters.per_page">
      <el-pagination
        v-model:current-page="filters.page"
        :page-size="filters.per_page"
        :total="total"
        layout="prev, pager, next"
        @current-change="fetchItems"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMyItems, deleteItem } from '@/api/items'
import ItemCard from '@/components/item/ItemCard.vue'

const router = useRouter()
const loading = ref(false)
const items = ref([])
const total = ref(0)

const filters = reactive({
  page: 1,
  per_page: 12,
  status: undefined,
})

async function fetchItems() {
  loading.value = true
  try {
    const res = await getMyItems(filters)
    items.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  try {
    await ElMessageBox.confirm('确定要删除该物品吗？', '提示')
    await deleteItem(id)
    ElMessage.success('删除成功')
    fetchItems()
  } catch {}
}

onMounted(fetchItems)
</script>

<style scoped>
.page-title { margin-bottom: 20px; }
.filter-row { margin-bottom: 20px; }
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
.item-wrap { display: flex; flex-direction: column; gap: 8px; }
.item-actions { display: flex; gap: 8px; justify-content: center; }
.pagination-wrap { display: flex; justify-content: center; margin-top: 32px; }
</style>

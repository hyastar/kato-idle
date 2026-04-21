<template>
  <div class="container page-padding">
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="filters.keyword"
        placeholder="搜索物品名称..."
        clearable
        size="large"
        @keyup.enter="handleSearch"
        @clear="handleSearch"
      >
        <template #append>
          <el-button @click="handleSearch">搜索</el-button>
        </template>
      </el-input>
    </div>

    <!-- 分类选择 -->
    <div class="category-bar">
      <el-tag
        :type="filters.category_id === null ? '' : 'info'"
        @click="selectCategory(null)"
        style="cursor:pointer; margin-right:8px"
      >全部</el-tag>
      <el-tag
        v-for="cat in categories"
        :key="cat.id"
        :type="filters.category_id === cat.id ? '' : 'info'"
        @click="selectCategory(cat.id)"
        style="cursor:pointer; margin-right:8px"
      >{{ cat.name }}</el-tag>
    </div>

    <!-- 筛选条件 -->
    <div class="filter-bar">
      <el-select v-model="filters.sort" @change="fetchItems" placeholder="排序" style="width:120px">
        <el-option label="最新发布" value="newest" />
        <el-option label="价格从低到高" value="price_asc" />
        <el-option label="价格从高到低" value="price_desc" />
        <el-option label="最多浏览" value="popular" />
      </el-select>

      <el-input-number v-model="filters.min_price" placeholder="最低价" :min="0" @change="fetchItems" />
      <span>—</span>
      <el-input-number v-model="filters.max_price" placeholder="最高价" :min="0" @change="fetchItems" />
    </div>

    <!-- 物品列表 -->
    <el-skeleton :loading="loading" animated>
      <template #default>
        <div class="items-grid" v-if="items.length">
          <ItemCard v-for="item in items" :key="item.id" :item="item" />
        </div>
        <el-empty v-else description="暂时没有物品" />
      </template>
    </el-skeleton>

    <!-- 分页 -->
    <div class="pagination-wrap">
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
import { useRoute } from 'vue-router'
import { getItemList } from '@/api/items'
import { getCategoryList } from '@/api/categories'
import ItemCard from '@/components/item/ItemCard.vue'

const route = useRoute()
const loading = ref(false)
const items = ref([])
const total = ref(0)
const categories = ref([])

const filters = reactive({
  page: 1,
  per_page: 12,
  keyword: '',
  category_id: null,
  min_price: undefined,
  max_price: undefined,
  sort: 'newest',
})

async function fetchItems() {
  loading.value = true
  try {
    const params = Object.fromEntries(
      Object.entries(filters).filter(([_, v]) => v !== null && v !== undefined && v !== '')
    )
    const res = await getItemList(params)
    items.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  filters.page = 1
  fetchItems()
}

function selectCategory(id) {
  filters.category_id = id
  filters.page = 1
  fetchItems()
}

onMounted(async () => {
  const catRes = await getCategoryList()
  categories.value = catRes.data
  if (route.query.keyword) {
    filters.keyword = route.query.keyword
  }
  fetchItems()
})
</script>

<style scoped>
.search-bar { margin: 20px 0; }
.category-bar { margin-bottom: 16px; }
.filter-bar { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
.pagination-wrap { display: flex; justify-content: center; margin-top: 32px; }
</style>

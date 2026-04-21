<template>
  <div class="item-filter">
    <el-input v-model="keyword" placeholder="搜索关键词" clearable @keyup.enter="$emit('search', keyword)" />
    <el-select v-model="selectedCategory" placeholder="分类" clearable @change="$emit('change')">
      <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
    </el-select>
    <el-select v-model="sort" @change="$emit('sort', sort)">
      <el-option label="最新" value="newest" />
      <el-option label="价格↑" value="price_asc" />
      <el-option label="价格↓" value="price_desc" />
      <el-option label="最热" value="popular" />
    </el-select>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({ categories: { type: Array, default: () => [] } })
defineEmits(['search', 'change', 'sort'])

const keyword = ref('')
const selectedCategory = ref(null)
const sort = ref('newest')
</script>

<style scoped>
.item-filter {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
</style>

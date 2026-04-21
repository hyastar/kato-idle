<template>
  <div class="container page-padding">
    <h2 class="page-title">购物车</h2>

    <el-skeleton :loading="loading" animated>
      <template #default>
        <div v-if="cartItems.length">
          <div class="cart-list">
            <div v-for="ci in cartItems" :key="ci.id" class="cart-item">
              <el-image :src="getImageUrl(ci.item?.cover)" fit="cover" class="item-image" />
              <div class="item-info">
                <p class="item-title">{{ ci.item?.title }}</p>
                <p class="item-price">¥{{ ci.item?.price }}</p>
                <p class="item-seller">{{ ci.item?.user?.nickname }}</p>
              </div>
              <div class="item-actions">
                <el-button size="small" @click="router.push(`/item/${ci.item_id}`)">查看详情</el-button>
                <el-button size="small" type="danger" @click="handleRemove(ci.item_id)">移除</el-button>
              </div>
            </div>
          </div>
          <div class="cart-footer">
            <el-button type="danger" @click="handleClear">清空购物车</el-button>
          </div>
        </div>
        <el-empty v-else description="购物车是空的" />
      </template>
    </el-skeleton>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getCart, removeFromCart, clearCart } from '@/api/cart'

const router = useRouter()
const loading = ref(false)
const cartItems = ref([])

function getImageUrl(path) {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `http://localhost:5000${path}`
}

async function fetchCart() {
  loading.value = true
  try {
    const res = await getCart()
    cartItems.value = res.data.items
  } finally {
    loading.value = false
  }
}

async function handleRemove(itemId) {
  try {
    await removeFromCart(itemId)
    ElMessage.success('已移除')
    fetchCart()
  } catch {}
}

async function handleClear() {
  try {
    await ElMessageBox.confirm('确定要清空购物车吗？', '提示')
    await clearCart()
    ElMessage.success('已清空')
    cartItems.value = []
  } catch {}
}

onMounted(fetchCart)
</script>

<style scoped>
.page-title { margin-bottom: 20px; }
.cart-list { display: flex; flex-direction: column; gap: 16px; }
.cart-item {
  display: flex;
  align-items: center;
  gap: 16px;
  background: white;
  padding: 16px;
  border-radius: 8px;
}
.item-image { width: 80px; height: 80px; border-radius: 6px; flex-shrink: 0; }
.item-info { flex: 1; }
.item-title { font-size: 16px; font-weight: bold; margin-bottom: 4px; }
.item-price { color: #f56c6c; font-size: 16px; font-weight: bold; }
.item-seller { font-size: 12px; color: #999; }
.item-actions { display: flex; flex-direction: column; gap: 8px; }
.cart-footer { margin-top: 20px; display: flex; justify-content: flex-end; }
</style>

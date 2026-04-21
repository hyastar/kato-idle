<template>
  <div class="container page-padding">
    <el-skeleton :loading="loading" animated>
      <template #default>
        <div v-if="item" class="item-detail">
          <!-- 图片展示 -->
          <div class="image-section">
            <el-image
              :src="getImageUrl(item.images[0])"
              fit="cover"
              class="main-image"
              :preview-src-list="item.images.map(getImageUrl)"
            >
              <template #error>
                <div class="image-placeholder">📦</div>
              </template>
            </el-image>
            <div class="thumbnail-list" v-if="item.images.length > 1">
              <el-image
                v-for="(img, idx) in item.images"
                :key="idx"
                :src="getImageUrl(img)"
                fit="cover"
                class="thumbnail"
                :class="{ active: idx === 0 }"
              />
            </div>
          </div>

          <!-- 信息区域 -->
          <div class="info-section">
            <h1 class="item-title">{{ item.title }}</h1>
            <div class="price-row">
              <span class="price">¥{{ item.price }}</span>
              <span class="original-price" v-if="item.original_price">原价: ¥{{ item.original_price }}</span>
            </div>
            <div class="meta-tags">
              <el-tag type="info">{{ item.condition_text }}</el-tag>
              <el-tag type="info" v-if="item.category">{{ item.category.name }}</el-tag>
              <el-tag type="warning" v-if="item.status === 2">已售出</el-tag>
            </div>
            <div class="seller-info">
              <el-avatar :src="getImageUrl(item.user?.avatar)" />
              <span>{{ item.user?.nickname }}</span>
            </div>
            <div class="detail-fields">
              <p v-if="item.description"><strong>描述：</strong>{{ item.description }}</p>
              <p v-if="item.contact"><strong>联系方式：</strong>{{ item.contact }}</p>
              <p v-if="item.location"><strong>交易地点：</strong>{{ item.location }}</p>
              <p><strong>发布时间：</strong>{{ item.created_at }}</p>
            </div>
            <div class="actions">
              <el-button type="primary" size="large" @click="handleAddCart" v-if="item.status === 1">
                加入购物车
              </el-button>
              <el-button type="danger" size="large" @click="handleFavorite">
                {{ isFavorited ? '取消收藏' : '收藏' }}
              </el-button>
            </div>
          </div>
        </div>
        <el-empty v-else description="物品不存在" />
      </template>
    </el-skeleton>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getItemDetail } from '@/api/items'
import { addFavorite, removeFavorite, checkFavorite } from '@/api/favorite'
import { addToCart } from '@/api/cart'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const item = ref(null)
const isFavorited = ref(false)

function getImageUrl(path) {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `http://localhost:5000${path}`
}

async function handleFavorite() {
  if (!userStore.isLoggedIn) return router.push('/login')
  try {
    if (isFavorited.value) {
      await removeFavorite(route.params.id)
      isFavorited.value = false
      ElMessage.success('已取消收藏')
    } else {
      await addFavorite(route.params.id)
      isFavorited.value = true
      ElMessage.success('收藏成功')
    }
  } catch {}
}

async function handleAddCart() {
  if (!userStore.isLoggedIn) return router.push('/login')
  try {
    await addToCart(route.params.id)
    ElMessage.success('已加入购物车')
  } catch {}
}

onMounted(async () => {
  loading.value = true
  try {
    const res = await getItemDetail(route.params.id)
    item.value = res.data
    if (userStore.isLoggedIn) {
      const favRes = await checkFavorite(route.params.id)
      isFavorited.value = favRes.data.is_favorited
    }
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.item-detail {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  background: white;
  padding: 24px;
  border-radius: 12px;
}
.image-section {}
.main-image { width: 100%; height: 400px; border-radius: 8px; }
.image-placeholder { width: 100%; height: 400px; display: flex; align-items: center; justify-content: center; background: #f5f5f5; font-size: 60px; border-radius: 8px; }
.thumbnail-list { display: flex; gap: 8px; margin-top: 12px; }
.thumbnail { width: 80px; height: 80px; border-radius: 4px; cursor: pointer; border: 2px solid transparent; }
.thumbnail.active { border-color: #409EFF; }
.info-section {}
.item-title { font-size: 22px; margin-bottom: 16px; }
.price-row { display: flex; align-items: baseline; gap: 12px; margin-bottom: 12px; }
.price { font-size: 28px; color: #f56c6c; font-weight: bold; }
.original-price { font-size: 14px; color: #999; text-decoration: line-through; }
.meta-tags { display: flex; gap: 8px; margin-bottom: 16px; }
.seller-info { display: flex; align-items: center; gap: 8px; padding: 12px 0; border-top: 1px solid #eee; border-bottom: 1px solid #eee; margin-bottom: 16px; }
.detail-fields { font-size: 14px; color: #666; line-height: 2; }
.actions { display: flex; gap: 12px; margin-top: 20px; }
</style>

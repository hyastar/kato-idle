<template>
  <header class="app-header">
    <div class="container header-inner">
      <RouterLink to="/" class="logo">🏫 校园二手</RouterLink>

      <el-input
        v-model="searchKeyword"
        placeholder="搜索物品..."
        clearable
        class="header-search"
        @keyup.enter="goSearch"
      />

      <div class="header-actions">
        <RouterLink to="/publish">
          <el-button type="primary" size="small">+ 发布物品</el-button>
        </RouterLink>

        <RouterLink to="/cart" v-if="isLoggedIn">
          <el-badge :value="cartCount" :hidden="cartCount === 0">
            <el-button :icon="ShoppingCart" circle />
          </el-badge>
        </RouterLink>

        <template v-if="!isLoggedIn">
          <RouterLink to="/login"><el-button>登录</el-button></RouterLink>
          <RouterLink to="/register"><el-button type="primary">注册</el-button></RouterLink>
        </template>

        <el-dropdown v-else @command="handleCommand">
          <el-avatar :src="getImageUrl(avatar)" style="cursor:pointer" />
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item command="my-items">我发布的</el-dropdown-item>
              <el-dropdown-item command="favorites">我的收藏</el-dropdown-item>
              <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ShoppingCart } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

const router = useRouter()
const userStore = useUserStore()
const { isLoggedIn, nickname, avatar } = storeToRefs(userStore)
const searchKeyword = ref('')
const cartCount = ref(0)

function getImageUrl(path) {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `http://localhost:5000${path}`
}

function goSearch() {
  if (searchKeyword.value.trim()) {
    router.push({ path: '/', query: { keyword: searchKeyword.value } })
  }
}

function handleCommand(cmd) {
  if (cmd === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示').then(() => {
      userStore.logout()
      ElMessage.success('已退出登录')
      router.push('/')
    }).catch(() => {})
  } else {
    const paths = { profile: '/profile', 'my-items': '/my-items', favorites: '/favorites' }
    router.push(paths[cmd])
  }
}
</script>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: 60px;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.header-inner {
  display: flex;
  align-items: center;
  height: 100%;
  gap: 16px;
}
.logo {
  font-size: 20px;
  font-weight: bold;
  color: #409EFF;
  text-decoration: none;
  white-space: nowrap;
}
.header-search {
  flex: 1;
  max-width: 400px;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
}
</style>

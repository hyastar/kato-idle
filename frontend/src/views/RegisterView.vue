<template>
  <div class="login-page">
    <div class="login-box">
      <h2 class="title">校园二手平台</h2>
      <p class="subtitle">注册新账号</p>

      <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
        <el-form-item label="用户名/学号" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名或学号" size="large" />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" placeholder="请输入昵称（选填）" size="large" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱（选填）" size="large" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码（至少6位）"
            size="large"
            show-password
            @keyup.enter="handleRegister"
          />
        </el-form-item>
        <el-button type="primary" size="large" :loading="loading" @click="handleRegister" style="width:100%">
          注 册
        </el-button>
      </el-form>

      <p class="login-link">
        已有账号？<RouterLink to="/login">立即登录</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref()
const loading = ref(false)
const form = ref({ username: '', nickname: '', email: '', password: '' })

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' },
  ],
}

async function handleRegister() {
  await formRef.value.validate()
  loading.value = true
  try {
    await userStore.register(form.value)
    ElMessage.success('注册成功！')
    router.push('/')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-box {
  background: white;
  padding: 40px;
  border-radius: 12px;
  width: 400px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}
.title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 8px;
  color: #333;
}
.subtitle {
  text-align: center;
  color: #999;
  margin-bottom: 24px;
}
.login-link {
  text-align: center;
  margin-top: 16px;
  color: #666;
  font-size: 14px;
}
</style>

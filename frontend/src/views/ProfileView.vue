<template>
  <div class="container page-padding">
    <el-card>
      <template #header>
        <h2>个人中心</h2>
      </template>

      <el-form :model="form" label-width="100px">
        <el-form-item label="头像">
          <el-upload
            :show-file-list="false"
            :auto-upload="false"
            :on-change="handleAvatarChange"
          >
            <el-avatar :src="getImageUrl(form.avatar)" :size="80" />
            <el-button size="small" style="margin-left:16px">更换头像</el-button>
          </el-upload>
        </el-form-item>

        <el-form-item label="用户名">
          <el-input v-model="form.username" disabled />
        </el-form-item>

        <el-form-item label="昵称">
          <el-input v-model="form.nickname" />
        </el-form-item>

        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>

        <el-form-item label="手机号">
          <el-input v-model="form.phone" />
        </el-form-item>

        <el-form-item label="校区">
          <el-input v-model="form.campus" placeholder="如：南湖校区" />
        </el-form-item>

        <el-form-item label="宿舍号">
          <el-input v-model="form.dorm" placeholder="如：3栋201" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSave">保存修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { getProfile, updateProfile, uploadAvatar } from '@/api/user'

const userStore = useUserStore()
const loading = ref(false)

const form = reactive({
  username: '',
  nickname: '',
  email: '',
  phone: '',
  campus: '',
  dorm: '',
  avatar: '',
})

function getImageUrl(path) {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `http://localhost:5000${path}`
}

async function handleSave() {
  loading.value = true
  try {
    await updateProfile(form)
    await userStore.refreshUserInfo()
    ElMessage.success('保存成功')
  } finally {
    loading.value = false
  }
}

async function handleAvatarChange(file) {
  const formData = new FormData()
  formData.append('avatar', file.raw)
  try {
    const res = await uploadAvatar(formData)
    form.avatar = res.data.avatar
    await userStore.refreshUserInfo()
    ElMessage.success('头像上传成功')
  } catch {}
}

onMounted(async () => {
  const res = await getProfile()
  Object.assign(form, res.data)
})
</script>

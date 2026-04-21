<template>
  <div class="container page-padding">
    <el-card>
      <template #header>
        <h2>发布物品</h2>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="物品名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入物品名称" />
        </el-form-item>

        <el-form-item label="分类" prop="category_id">
          <el-select v-model="form.category_id" placeholder="请选择分类">
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>

        <el-form-item label="新旧程度" prop="condition">
          <el-select v-model="form.condition" placeholder="请选择新旧程度">
            <el-option v-for="opt in conditionOptions" :key="opt.value" :label="opt.label" :value="opt.value" />
          </el-select>
        </el-form-item>

        <el-form-item label="价格" prop="price">
          <el-input-number v-model="form.price" :min="0" :precision="2" placeholder="请输入价格" />
        </el-form-item>

        <el-form-item label="原价（选填）">
          <el-input-number v-model="form.original_price" :min="0" :precision="2" placeholder="原价" />
        </el-form-item>

        <el-form-item label="物品描述">
          <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请输入物品描述" />
        </el-form-item>

        <el-form-item label="联系方式">
          <el-input v-model="form.contact" placeholder="请输入联系方式" />
        </el-form-item>

        <el-form-item label="交易地点">
          <el-input v-model="form.location" placeholder="请输入交易地点" />
        </el-form-item>

        <el-form-item label="上传图片">
          <el-upload
            v-model:file-list="fileList"
            action="#"
            :auto-upload="false"
            :limit="6"
            list-type="picture-card"
            multiple
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">发布物品</el-button>
          <el-button @click="router.push('/')">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { createItem } from '@/api/items'
import { getCategoryList } from '@/api/categories'

const router = useRouter()
const formRef = ref()
const loading = ref(false)
const categories = ref([])
const fileList = ref([])

const form = reactive({
  title: '',
  description: '',
  price: null,
  original_price: null,
  category_id: null,
  condition: 1,
  contact: '',
  location: '',
})

const rules = {
  title: [{ required: true, message: '请填写物品名称', trigger: 'blur' }],
  price: [{ required: true, message: '请填写价格', trigger: 'blur' }],
  category_id: [{ required: true, message: '请选择分类', trigger: 'change' }],
  condition: [{ required: true, message: '请选择新旧程度', trigger: 'change' }],
}

const conditionOptions = [
  { value: 1, label: '全新' },
  { value: 2, label: '几乎全新' },
  { value: 3, label: '有使用痕迹' },
  { value: 4, label: '功能完好' },
  { value: 5, label: '有明显磨损' },
]

async function handleSubmit() {
  await formRef.value.validate()
  loading.value = true
  try {
    const formData = new FormData()
    Object.entries(form).forEach(([key, val]) => {
      if (val !== null && val !== '') formData.append(key, val)
    })
    fileList.value.forEach(f => {
      if (f.raw) formData.append('images', f.raw)
    })
    await createItem(formData)
    ElMessage.success('发布成功！')
    router.push('/')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const res = await getCategoryList()
  categories.value = res.data
})
</script>

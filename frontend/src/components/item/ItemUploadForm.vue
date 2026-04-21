<template>
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
      <el-input-number v-model="form.price" :min="0" :precision="2" />
    </el-form-item>
    <el-form-item label="描述">
      <el-input v-model="form.description" type="textarea" :rows="3" />
    </el-form-item>
    <el-form-item>
      <slot>
        <el-button type="primary" @click="$emit('submit', form)">提交</el-button>
      </slot>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, reactive } from 'vue'

const props = defineProps({
  modelValue: { type: Object, default: () => ({}) },
  categories: { type: Array, default: () => [] }
})
defineEmits(['submit'])

const formRef = ref()
const form = reactive({ ...props.modelValue })

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
</script>

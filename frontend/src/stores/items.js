import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useItemsStore = defineStore('items', () => {
  const list = ref([])
  const total = ref(0)
  const loading = ref(false)

  function setList(data) {
    list.value = data
  }

  function setTotal(count) {
    total.value = count
  }

  function setLoading(val) {
    loading.value = val
  }

  return { list, total, loading, setList, setTotal, setLoading }
})

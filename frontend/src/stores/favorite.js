import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getFavorites, addFavorite, removeFavorite } from '@/api/favorite'

export const useFavoriteStore = defineStore('favorite', () => {
  const items = ref([])
  const loading = ref(false)

  async function fetchFavorites() {
    loading.value = true
    try {
      const res = await getFavorites()
      items.value = res.data
    } finally {
      loading.value = false
    }
  }

  async function toggle(itemId) {
    const exists = items.value.some(f => f.item_id === itemId)
    if (exists) {
      await removeFavorite(itemId)
    } else {
      await addFavorite(itemId)
    }
    await fetchFavorites()
  }

  return { items, loading, fetchFavorites, toggle }
})

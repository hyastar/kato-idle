import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getCart, addToCart, removeFromCart, clearCart } from '@/api/cart'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const loading = ref(false)

  async function fetchCart() {
    loading.value = true
    try {
      const res = await getCart()
      items.value = res.data.items
    } finally {
      loading.value = false
    }
  }

  async function addCart(itemId) {
    await addToCart(itemId)
    await fetchCart()
  }

  async function removeCart(itemId) {
    await removeFromCart(itemId)
    await fetchCart()
  }

  async function clear() {
    await clearCart()
    items.value = []
  }

  return { items, loading, fetchCart, addCart, removeCart, clear }
})

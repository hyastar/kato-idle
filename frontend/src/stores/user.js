import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, register as registerApi, getUserInfo } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('kato_token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('kato_user') || 'null'))

  const isLoggedIn = computed(() => !!token.value)
  const userId = computed(() => userInfo.value?.id ?? null)
  const nickname = computed(() => userInfo.value?.nickname || '用户')
  const avatar = computed(() => userInfo.value?.avatar || '')

  async function login(credentials) {
    const res = await loginApi(credentials)
    setAuth(res.data.token, res.data.user)
    return res
  }

  async function register(form) {
    const res = await registerApi(form)
    setAuth(res.data.token, res.data.user)
    return res
  }

  async function refreshUserInfo() {
    const res = await getUserInfo()
    userInfo.value = res.data
    localStorage.setItem('kato_user', JSON.stringify(res.data))
  }

  function setAuth(newToken, user) {
    token.value = newToken
    userInfo.value = user
    localStorage.setItem('kato_token', newToken)
    localStorage.setItem('kato_user', JSON.stringify(user))
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('kato_token')
    localStorage.removeItem('kato_user')
  }

  return {
    token, userInfo, isLoggedIn, userId, nickname, avatar,
    login, register, logout, refreshUserInfo
  }
})

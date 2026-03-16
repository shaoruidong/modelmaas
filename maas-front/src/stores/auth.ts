import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => user.value !== null)

  function login(username: string, password: string): { success: boolean; error?: string } {
    if (username === 'admin' && password === 'admin') {
      user.value = { id: '1', username: 'admin', role: 'admin' }
      return { success: true }
    }
    return { success: false, error: '用户名或密码错误' }
  }

  function logout() {
    user.value = null
  }

  return { user, isAuthenticated, login, logout }
})

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import request from '@/utils/request'

export interface AuthUser {
  id: number
  phone: string
  role: string
}

export const useAuthStore = defineStore('auth', () => {
  // 初始化时从 localStorage 恢复用户信息（刷新页面不丢失登录态）
  const user = ref<AuthUser | null>(
    JSON.parse(localStorage.getItem('user') ?? 'null'),
  )

  const isAuthenticated = computed(() => user.value !== null)

  async function login(
    phone: string,
    password: string,
  ): Promise<{ success: boolean; error?: string }> {
    try {
      const { data } = await request.post('/auth/login/', { phone, password })
      // 后端返回：{ access, refresh, user: { id, phone, role } }
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      user.value = data.user
      localStorage.setItem('user', JSON.stringify(data.user))
      return { success: true }
    } catch (err: any) {
      const data = err.response?.data
      const msg =
        data?.detail ||
        data?.non_field_errors?.[0] ||
        data?.phone?.[0] ||
        data?.password?.[0] ||
        '登录失败，请稍后重试'
      return { success: false, error: msg }
    }
  }

  function logout() {
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  }

  return { user, isAuthenticated, login, logout }
})

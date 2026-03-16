<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const form = reactive({ username: '', password: '' })
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  if (!form.username || !form.password) {
    error.value = '请输入用户名和密码'
    return
  }
  loading.value = true
  await new Promise((r) => setTimeout(r, 600))
  const result = auth.login(form.username, form.password)
  loading.value = false
  if (result.success) {
    router.push('/dashboard')
  } else {
    error.value = result.error ?? '登录失败'
  }
}
</script>

<template>
  <div class="login-page">
    <!-- Animated background -->
    <div class="bg-animation">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
      <div class="grid-overlay"></div>
    </div>

    <!-- Login card -->
    <div class="login-card">
      <div class="login-logo">
        <div class="logo-mark">M</div>
        <div class="logo-info">
          <div class="logo-name">MaaS 平台</div>
          <div class="logo-sub">Model as a Service</div>
        </div>
      </div>

      <h2 class="login-title">欢迎回来</h2>
      <p class="login-desc">登录以访问大模型管理平台</p>

      <el-form @submit.prevent="handleLogin" class="login-form">
        <el-form-item>
          <el-input
            v-model="form.username"
            placeholder="用户名"
            size="large"
            prefix-icon="User"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            size="large"
            prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <transition name="fade">
          <div v-if="error" class="login-error">
            <el-icon><WarningFilled /></el-icon>
            {{ error }}
          </div>
        </transition>

        <el-button
          type="primary"
          size="large"
          :loading="loading"
          class="login-btn"
          @click="handleLogin"
        >
          {{ loading ? '登录中...' : '登 录' }}
        </el-button>
      </el-form>

      <div class="login-hint">默认账号：admin / admin</div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-primary);
  position: relative;
  overflow: hidden;
}

/* Animated orbs */
.bg-animation {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.35;
  animation: float 8s ease-in-out infinite;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #1677ff, transparent);
  top: -150px;
  left: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, #7c3aed, transparent);
  bottom: -100px;
  right: -80px;
  animation-delay: -3s;
}

.orb-3 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, #06b6d4, transparent);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -6s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-30px) scale(1.05);
  }
}

.orb-3 {
  animation: float3 10s ease-in-out infinite;
}

@keyframes float3 {
  0%,
  100% {
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    transform: translate(-50%, -60%) scale(1.1);
  }
}

/* Grid overlay */
.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(22, 119, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(22, 119, 255, 0.04) 1px, transparent 1px);
  background-size: 40px 40px;
}

/* Login card */
.login-card {
  position: relative;
  z-index: 10;
  width: 420px;
  background: rgba(17, 24, 39, 0.85);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-xl);
  padding: 40px;
  box-shadow:
    0 24px 64px rgba(0, 0, 0, 0.6),
    0 0 0 1px rgba(22, 119, 255, 0.1);
}

.login-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 28px;
}

.logo-mark {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: var(--gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 800;
  color: #fff;
  box-shadow: var(--shadow-glow);
}

.logo-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.logo-sub {
  font-size: 11px;
  color: var(--color-text-muted);
  letter-spacing: 0.05em;
}

.login-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 6px;
}

.login-desc {
  font-size: 13px;
  color: var(--color-text-muted);
  margin-bottom: 28px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.login-form :deep(.el-input__wrapper) {
  background: rgba(26, 34, 53, 0.8) !important;
  border: 1px solid var(--color-border) !important;
  border-radius: var(--radius-sm) !important;
  box-shadow: none !important;
  transition:
    border-color var(--transition-fast),
    box-shadow var(--transition-fast) !important;
}

.login-form :deep(.el-input__wrapper:hover),
.login-form :deep(.el-input__wrapper.is-focus) {
  border-color: var(--color-accent) !important;
  box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.2) !important;
}

.login-form :deep(.el-input__inner) {
  color: var(--color-text-primary) !important;
}

.login-form :deep(.el-input__prefix-icon) {
  color: var(--color-text-muted) !important;
}

.login-error {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--color-danger);
  font-size: 13px;
  padding: 8px 12px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: var(--radius-sm);
  margin-bottom: 4px;
}

.login-btn {
  width: 100%;
  height: 44px;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.1em;
  background: var(--gradient-primary) !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  margin-top: 8px;
  transition: all var(--transition-fast) !important;
}

.login-btn:hover {
  box-shadow: var(--shadow-glow-hover) !important;
  transform: translateY(-1px);
}

.login-hint {
  text-align: center;
  font-size: 12px;
  color: var(--color-text-muted);
  margin-top: 20px;
}
</style>

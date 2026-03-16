<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const emit = defineEmits<{ toggleSidebar: [] }>()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const breadcrumb = computed(() => {
  const map: Record<string, string> = {
    dashboard: '控制台',
    models: '模型广场',
    'model-detail': '模型详情',
    'fine-tuning': '模型微调',
    data: '数据管理',
    'api-keys': 'API Key 管理',
    inference: '在线推理',
    analytics: '统计看板',
  }
  return map[route.name as string] ?? '控制台'
})

function handleCommand(cmd: string) {
  if (cmd === 'logout') {
    auth.logout()
    router.push('/login')
  }
}
</script>

<template>
  <header class="app-header">
    <div class="header-left">
      <el-button text @click="emit('toggleSidebar')" class="toggle-btn">
        <el-icon size="18"><Fold /></el-icon>
      </el-button>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>{{ breadcrumb }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="header-right">
      <el-tooltip content="文档中心" placement="bottom">
        <el-button text circle>
          <el-icon size="18"><Document /></el-icon>
        </el-button>
      </el-tooltip>
      <el-tooltip content="消息通知" placement="bottom">
        <el-button text circle>
          <el-icon size="18"><Bell /></el-icon>
        </el-button>
      </el-tooltip>

      <el-dropdown @command="handleCommand" trigger="click">
        <div class="user-avatar">
          <span>{{ auth.user?.username?.charAt(0).toUpperCase() }}</span>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item disabled>
              <el-icon><User /></el-icon>
              {{ auth.user?.username }}
            </el-dropdown-item>
            <el-dropdown-item divided command="logout">
              <el-icon><SwitchButton /></el-icon>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  height: var(--header-height);
  background: var(--color-bg-header);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-lg);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 100;
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.toggle-btn {
  color: var(--color-text-secondary) !important;
}

.toggle-btn:hover {
  color: var(--color-accent) !important;
}

:deep(.el-breadcrumb__inner) {
  color: var(--color-text-secondary) !important;
}

:deep(.el-breadcrumb__item:last-child .el-breadcrumb__inner) {
  color: var(--color-text-primary) !important;
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.header-right .el-button {
  color: var(--color-text-secondary) !important;
}

.header-right .el-button:hover {
  color: var(--color-accent) !important;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  color: #fff;
  cursor: pointer;
  transition: box-shadow var(--transition-fast);
}

.user-avatar:hover {
  box-shadow: var(--shadow-glow);
}
</style>

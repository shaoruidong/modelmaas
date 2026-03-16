<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps<{ collapsed: boolean }>()
defineEmits<{ 'update:collapsed': [value: boolean] }>()

const route = useRoute()

const navGroups = [
  {
    label: '模型广场',
    items: [
      { key: 'models', label: '模型广场', icon: 'Grid', path: '/models' },
      { key: 'inference', label: '模型体验', icon: 'ChatDotRound', path: '/inference' },
    ],
  },
  {
    label: '模型训练',
    items: [{ key: 'fine-tuning', label: '模型微调', icon: 'Setting', path: '/fine-tuning' }],
  },
  {
    label: '数据管理',
    items: [{ key: 'data', label: '数据管理', icon: 'FolderOpened', path: '/data' }],
  },
  {
    label: '安全工具',
    items: [{ key: 'safety', label: '敏感词管理', icon: 'Shield', path: '/safety' }],
  },
  {
    label: '工具应用',
    items: [{ key: 'api-keys', label: 'API Key', icon: 'Key', path: '/api-keys' }],
  },
  {
    label: '统计看板',
    items: [{ key: 'analytics', label: '统计看板', icon: 'TrendCharts', path: '/analytics' }],
  },
]

const activeKey = computed(() => {
  const path = route.path
  for (const group of navGroups) {
    for (const item of group.items) {
      if (path.startsWith(item.path)) return item.key
    }
  }
  return 'dashboard'
})
</script>

<template>
  <aside class="sidebar" :class="{ collapsed }">
    <!-- Logo -->
    <div class="sidebar-logo">
      <div class="logo-icon">M</div>
      <transition name="fade">
        <span v-if="!collapsed" class="logo-text">MaaS 平台</span>
      </transition>
    </div>

    <!-- Dashboard shortcut -->
    <router-link
      to="/dashboard"
      class="nav-item"
      :class="{ active: route.path === '/dashboard', collapsed }"
    >
      <el-icon><HomeFilled /></el-icon>
      <transition name="fade">
        <span v-if="!collapsed" class="nav-label">控制台</span>
      </transition>
    </router-link>

    <!-- Nav groups -->
    <div v-for="group in navGroups" :key="group.label" class="nav-group">
      <transition name="fade">
        <div v-if="!collapsed" class="nav-group-label">{{ group.label }}</div>
      </transition>
      <el-tooltip
        v-for="item in group.items"
        :key="item.key"
        :content="item.label"
        placement="right"
        :disabled="!collapsed"
      >
        <router-link
          :to="item.path"
          class="nav-item"
          :class="{ active: activeKey === item.key, collapsed }"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          <transition name="fade">
            <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
          </transition>
        </router-link>
      </el-tooltip>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  min-height: 100vh;
  background: var(--color-bg-sidebar);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  transition: width var(--transition-normal);
  overflow: hidden;
  flex-shrink: 0;
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

.sidebar-logo {
  height: var(--header-height);
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 16px;
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}

.logo-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  color: #fff;
  flex-shrink: 0;
}

.logo-text {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
  white-space: nowrap;
}

.nav-group {
  margin-top: 4px;
}

.nav-group-label {
  font-size: 11px;
  color: var(--color-text-muted);
  padding: 12px 16px 4px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 16px;
  color: var(--color-text-secondary);
  text-decoration: none;
  border-radius: var(--radius-sm);
  margin: 2px 8px;
  transition: all var(--transition-fast);
  white-space: nowrap;
  cursor: pointer;
}

.nav-item:hover {
  background: var(--color-accent-light);
  color: var(--color-text-accent);
}

.nav-item.active {
  background: var(--color-accent-light);
  color: var(--color-accent);
  border-left: 2px solid var(--color-accent);
}

.nav-item.collapsed {
  justify-content: center;
  padding: 9px;
  margin: 2px auto;
  width: 40px;
}

.nav-label {
  font-size: 13px;
  white-space: nowrap;
}

.el-icon {
  font-size: 16px;
  flex-shrink: 0;
}
</style>

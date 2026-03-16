<script setup lang="ts">
defineProps<{
  title: string
  value: number | string
  icon: string
  trend?: number
  color?: string
}>()
</script>

<template>
  <div class="metric-card">
    <div class="metric-icon" :style="{ background: color ?? 'var(--gradient-primary)' }">
      <el-icon size="20"><component :is="icon" /></el-icon>
    </div>
    <div class="metric-body">
      <div class="metric-value">
        {{ typeof value === 'number' ? value.toLocaleString() : value }}
      </div>
      <div class="metric-title">{{ title }}</div>
    </div>
    <div v-if="trend !== undefined" class="metric-trend" :class="trend >= 0 ? 'up' : 'down'">
      <el-icon><component :is="trend >= 0 ? 'ArrowUp' : 'ArrowDown'" /></el-icon>
      {{ Math.abs(trend) }}%
    </div>
  </div>
</template>

<style scoped>
.metric-card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  transition: all var(--transition-normal);
  cursor: default;
}

.metric-card:hover {
  border-color: var(--color-border-active);
  box-shadow: var(--shadow-glow);
  transform: translateY(-2px);
}

.metric-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
}

.metric-body {
  flex: 1;
}

.metric-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.metric-title {
  font-size: 12px;
  color: var(--color-text-muted);
  margin-top: 2px;
}

.metric-trend {
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 2px;
}

.metric-trend.up {
  color: var(--color-success);
}
.metric-trend.down {
  color: var(--color-danger);
}
</style>

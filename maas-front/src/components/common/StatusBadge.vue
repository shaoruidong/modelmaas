<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ status: string }>()

const config = computed(() => {
  const map: Record<
    string,
    { type: 'success' | 'warning' | 'danger' | 'info' | ''; label: string }
  > = {
    已完成: { type: 'success', label: '已完成' },
    运行中: { type: 'warning', label: '运行中' },
    待运行: { type: 'info', label: '待运行' },
    失败: { type: 'danger', label: '失败' },
    active: { type: 'success', label: '启用' },
    disabled: { type: 'danger', label: '禁用' },
    available: { type: 'success', label: '可用' },
    deprecated: { type: 'info', label: '已废弃' },
  }
  return map[props.status] ?? { type: '' as const, label: props.status }
})
</script>

<template>
  <el-tag :type="config.type" size="small" effect="dark">{{ config.label }}</el-tag>
</template>

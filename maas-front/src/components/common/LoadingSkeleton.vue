<script setup lang="ts">
defineProps<{ count?: number }>()
</script>

<template>
  <div class="skeleton-grid">
    <div v-for="i in count ?? 6" :key="i" class="skeleton-card">
      <el-skeleton animated>
        <template #template>
          <div style="padding: 16px">
            <el-skeleton-item variant="h3" style="width: 60%; margin-bottom: 12px" />
            <el-skeleton-item variant="text" style="width: 100%; margin-bottom: 8px" />
            <el-skeleton-item variant="text" style="width: 80%" />
            <div style="display: flex; gap: 8px; margin-top: 12px">
              <el-skeleton-item variant="button" style="width: 60px; height: 22px" />
              <el-skeleton-item variant="button" style="width: 60px; height: 22px" />
            </div>
          </div>
        </template>
      </el-skeleton>
    </div>
  </div>
</template>

<style scoped>
.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--spacing-md);
}

.skeleton-card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}
</style>

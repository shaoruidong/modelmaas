<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useModelStore } from '@/stores/models'
import LoadingSkeleton from '@/components/common/LoadingSkeleton.vue'
import type { ModelCategory } from '@/types'

const router = useRouter()
const store = useModelStore()

const categories: { label: string; value: ModelCategory | '' }[] = [
  { label: '全部', value: '' },
  { label: '文本模型', value: 'text' },
  { label: '视觉模型', value: 'vision' },
  { label: '语音模型', value: 'audio' },
  { label: '多模态', value: 'multimodal' },
  { label: '向量模型', value: 'embedding' },
]

const categoryColorMap: Record<string, string> = {
  text: '#1677ff',
  vision: '#7c3aed',
  audio: '#059669',
  multimodal: '#f59e0b',
  embedding: '#ef4444',
}
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">模型广场</h1>
      <el-input
        v-model="store.searchKeyword"
        placeholder="搜索模型名称或描述..."
        prefix-icon="Search"
        clearable
        style="width: 280px"
      />
    </div>

    <!-- Category tabs -->
    <div class="category-tabs">
      <button
        v-for="cat in categories"
        :key="cat.value"
        class="cat-tab"
        :class="{ active: store.selectedCategory === cat.value }"
        @click="store.selectedCategory = cat.value"
      >
        {{ cat.label }}
      </button>
    </div>

    <!-- Loading skeleton -->
    <LoadingSkeleton v-if="store.loading" :count="6" />

    <!-- Model grid -->
    <div v-else class="model-grid">
      <div
        v-for="model in store.filteredModels"
        :key="model.id"
        class="model-card"
        @click="router.push(`/models/${model.id}`)"
      >
        <div class="model-card-header">
          <div
            class="model-avatar"
            :style="{
              background: `linear-gradient(135deg, ${categoryColorMap[model.category]}, ${categoryColorMap[model.category]}88)`,
            }"
          >
            {{ model.name.charAt(0) }}
          </div>
          <div class="model-meta">
            <div class="model-name">{{ model.name }}</div>
            <div class="model-provider">{{ model.provider }} · {{ model.parameterSize }}</div>
          </div>
          <el-tag
            size="small"
            effect="dark"
            :color="categoryColorMap[model.category] + '33'"
            style="border: none"
          >
            {{ model.category }}
          </el-tag>
        </div>
        <p class="model-desc">{{ model.description }}</p>
        <div class="model-tags">
          <el-tag
            v-for="tag in model.tags"
            :key="tag"
            size="small"
            effect="plain"
            class="model-tag"
          >
            {{ tag }}
          </el-tag>
        </div>
        <div class="model-footer">
          <el-button size="small" type="primary" plain @click.stop="router.push('/inference')">
            在线体验
          </el-button>
          <el-button size="small" plain @click.stop="router.push(`/models/${model.id}`)">
            查看详情
          </el-button>
        </div>
      </div>

      <div v-if="store.filteredModels.length === 0" class="empty-state">
        <el-icon size="48" color="var(--color-text-muted)"><Search /></el-icon>
        <p>未找到匹配的模型</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.category-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: var(--spacing-lg);
  flex-wrap: wrap;
}

.cat-tab {
  padding: 6px 16px;
  border-radius: 20px;
  border: 1px solid var(--color-border);
  background: transparent;
  color: var(--color-text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.cat-tab:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.cat-tab.active {
  background: var(--color-accent-light);
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.model-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-md);
}

.model-card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.model-card:hover {
  border-color: var(--color-border-active);
  box-shadow: var(--shadow-glow);
  transform: translateY(-2px);
}

.model-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.model-avatar {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
}

.model-meta {
  flex: 1;
  min-width: 0;
}

.model-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.model-provider {
  font-size: 12px;
  color: var(--color-text-muted);
  margin-top: 2px;
}

.model-desc {
  font-size: 13px;
  color: var(--color-text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.model-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.model-tag {
  font-size: 11px !important;
  border-color: var(--color-border) !important;
  color: var(--color-text-muted) !important;
  background: transparent !important;
}

.model-footer {
  display: flex;
  gap: 8px;
  margin-top: auto;
}

.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 60px;
  color: var(--color-text-muted);
  font-size: 14px;
}
</style>

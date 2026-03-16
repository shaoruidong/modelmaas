<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useModelStore } from '@/stores/models'
import StatusBadge from '@/components/common/StatusBadge.vue'

const route = useRoute()
const router = useRouter()
const store = useModelStore()

const model = computed(() => store.models.find((m) => m.id === route.params.id))
</script>

<template>
  <div class="page-container">
    <div v-if="model">
      <div class="page-header">
        <div style="display: flex; align-items: center; gap: 12px">
          <el-button text @click="router.back()"
            ><el-icon><ArrowLeft /></el-icon> 返回</el-button
          >
          <h1 class="page-title">{{ model.name }}</h1>
          <StatusBadge :status="model.status" />
        </div>
        <el-button type="primary" @click="router.push('/inference')">在线体验</el-button>
      </div>

      <div class="detail-grid">
        <div class="detail-main maas-card">
          <h3 class="section-label">模型简介</h3>
          <p class="detail-desc">{{ model.description }}</p>
          <div class="detail-tags">
            <el-tag v-for="tag in model.tags" :key="tag" effect="dark" style="margin-right: 8px">{{
              tag
            }}</el-tag>
          </div>
        </div>

        <div class="detail-info maas-card">
          <h3 class="section-label">基本信息</h3>
          <div class="info-row">
            <span>提供商</span><span>{{ model.provider }}</span>
          </div>
          <div class="info-row">
            <span>参数量</span><span>{{ model.parameterSize }}</span>
          </div>
          <div class="info-row">
            <span>模型类型</span><span>{{ model.category }}</span>
          </div>
          <div class="info-row">
            <span>上线时间</span><span>{{ model.createdAt }}</span>
          </div>
          <div class="info-row"><span>状态</span><StatusBadge :status="model.status" /></div>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <p>模型不存在</p>
      <el-button @click="router.push('/models')">返回模型广场</el-button>
    </div>
  </div>
</template>

<style scoped>
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: var(--spacing-md);
}

.section-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--color-border);
}

.detail-desc {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.8;
  margin-bottom: 16px;
}

.detail-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid var(--color-border);
  font-size: 13px;
}

.info-row:last-child {
  border-bottom: none;
}
.info-row span:first-child {
  color: var(--color-text-muted);
}
.info-row span:last-child {
  color: var(--color-text-primary);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 80px;
  color: var(--color-text-muted);
}
</style>

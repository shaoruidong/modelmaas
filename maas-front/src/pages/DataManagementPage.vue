<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { useDatasetStore } from '@/stores/datasets'
import StatusBadge from '@/components/common/StatusBadge.vue'
import { validateRequired, formatFileSize } from '@/utils/validation'

const store = useDatasetStore()

const dialogVisible = ref(false)
const formErrors = ref<string[]>([])

const form = reactive({
  name: '',
  description: '',
  type: 'text' as 'text' | 'image' | 'audio' | 'multimodal',
})

function openCreate() {
  form.name = ''
  form.description = ''
  form.type = 'text'
  formErrors.value = []
  dialogVisible.value = true
}

function submitDataset() {
  formErrors.value = []
  const errs = validateRequired({ 数据集名称: form.name, 数据类型: form.type })
  if (errs.length) {
    formErrors.value = errs
    return
  }
  store.createDataset({ name: form.name, description: form.description, type: form.type })
  dialogVisible.value = false
  ElMessage.success('数据集创建成功')
}

async function confirmDelete(id: string, name: string) {
  try {
    await ElMessageBox.confirm(`确认删除数据集「${name}」？此操作不可撤销。`, '删除确认', {
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      type: 'warning',
    })
    store.deleteDataset(id)
    ElMessage.success('已删除')
  } catch {
    // cancelled
  }
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('zh-CN')
}
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">数据管理</h1>
      <el-button type="primary" @click="openCreate">
        <el-icon><Plus /></el-icon> 新建数据集
      </el-button>
    </div>

    <!-- Stats row -->
    <div class="stats-row">
      <div class="stat-item">
        <span class="stat-value">{{ store.datasets.length }}</span>
        <span class="stat-label">数据集总数</span>
      </div>
      <div class="stat-item">
        <span class="stat-value">{{ store.datasets.filter((d) => d.type === 'text').length }}</span>
        <span class="stat-label">文本数据集</span>
      </div>
      <div class="stat-item">
        <span class="stat-value">{{
          store.datasets.reduce((s, d) => s + d.recordCount, 0).toLocaleString()
        }}</span>
        <span class="stat-label">总数据条数</span>
      </div>
    </div>

    <!-- Table -->
    <div class="maas-card" style="padding: 0; overflow: hidden">
      <el-table :data="store.datasets" style="width: 100%">
        <el-table-column prop="name" label="数据集名称" min-width="180" />
        <el-table-column label="类型" width="100">
          <template #default="{ row }">
            <StatusBadge :status="row.type" />
          </template>
        </el-table-column>
        <el-table-column label="数据量" width="120">
          <template #default="{ row }">{{ row.recordCount.toLocaleString() }} 条</template>
        </el-table-column>
        <el-table-column label="大小" width="100">
          <template #default="{ row }">{{ formatFileSize(row.size) }}</template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column label="创建时间" width="120">
          <template #default="{ row }">{{ formatDate(row.createdAt) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button size="small" text type="danger" @click="confirmDelete(row.id, row.name)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- Create dialog -->
    <el-dialog
      v-model="dialogVisible"
      title="新建数据集"
      width="480px"
      :close-on-click-modal="false"
    >
      <el-form label-width="90px">
        <el-form-item label="数据集名称" required>
          <el-input v-model="form.name" placeholder="请输入数据集名称" />
        </el-form-item>
        <el-form-item label="数据类型" required>
          <el-select v-model="form.type" style="width: 100%">
            <el-option label="文本" value="text" />
            <el-option label="图像" value="image" />
            <el-option label="音频" value="audio" />
            <el-option label="多模态" value="multimodal" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入数据集描述（可选）"
          />
        </el-form-item>
      </el-form>

      <div v-if="formErrors.length" class="form-errors">
        <el-icon><WarningFilled /></el-icon>
        {{ formErrors.join('；') }}
      </div>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitDataset">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.stats-row {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.stat-item {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 16px 24px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 140px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-accent);
}

.stat-label {
  font-size: 12px;
  color: var(--color-text-muted);
}

.form-errors {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--color-danger);
  font-size: 13px;
  padding: 8px 12px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: var(--radius-sm);
  margin-top: 12px;
}
</style>

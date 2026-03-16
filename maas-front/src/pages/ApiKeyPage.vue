<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { useApiKeyStore } from '@/stores/apikeys'
import StatusBadge from '@/components/common/StatusBadge.vue'
import { validateRequired } from '@/utils/validation'

const store = useApiKeyStore()

const createDialogVisible = ref(false)
const keyRevealVisible = ref(false)
const newKeyName = ref('')
const formErrors = ref<string[]>([])

function openCreate() {
  newKeyName.value = ''
  formErrors.value = []
  createDialogVisible.value = true
}

function submitCreate() {
  formErrors.value = []
  const errs = validateRequired({ 'Key 名称': newKeyName.value })
  if (errs.length) {
    formErrors.value = errs
    return
  }
  store.createApiKey(newKeyName.value)
  createDialogVisible.value = false
  keyRevealVisible.value = true
}

function copyKey(text: string) {
  navigator.clipboard.writeText(text).then(() => {
    ElMessage.success('已复制到剪贴板')
  })
}

function closeReveal() {
  store.clearLastKey()
  keyRevealVisible.value = false
}

async function confirmDelete(id: string, name: string) {
  try {
    await ElMessageBox.confirm(`确认删除 API Key「${name}」？删除后将无法恢复。`, '删除确认', {
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      type: 'warning',
    })
    store.deleteApiKey(id)
    ElMessage.success('已删除')
  } catch {
    // cancelled
  }
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('zh-CN')
}

// Watch for dialog close to clear key
watch(keyRevealVisible, (v) => {
  if (!v) store.clearLastKey()
})
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <div>
        <h1 class="page-title">API Key 管理</h1>
        <p style="font-size: 13px; color: var(--color-text-muted); margin-top: 4px">
          管理用于调用模型服务的访问密钥
        </p>
      </div>
      <el-button type="primary" @click="openCreate">
        <el-icon><Plus /></el-icon> 新建 API Key
      </el-button>
    </div>

    <!-- Keys table -->
    <div class="maas-card" style="padding: 0; overflow: hidden">
      <el-table :data="store.apiKeys" style="width: 100%">
        <el-table-column prop="name" label="名称" min-width="160" />
        <el-table-column label="Key" min-width="280">
          <template #default="{ row }">
            <div class="key-cell">
              <code class="key-code">{{ row.maskedKey }}</code>
              <el-tooltip content="复制" placement="top">
                <el-button text size="small" @click="copyKey(row.maskedKey)">
                  <el-icon><CopyDocument /></el-icon>
                </el-button>
              </el-tooltip>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <StatusBadge :status="row.status" />
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="120">
          <template #default="{ row }">{{ formatDate(row.createdAt) }}</template>
        </el-table-column>
        <el-table-column label="最后使用" width="120">
          <template #default="{ row }">
            {{ row.lastUsedAt ? formatDate(row.lastUsedAt) : '—' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
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
      v-model="createDialogVisible"
      title="新建 API Key"
      width="440px"
      :close-on-click-modal="false"
    >
      <el-form label-width="80px">
        <el-form-item label="Key 名称" required>
          <el-input
            v-model="newKeyName"
            placeholder="例如：生产环境-主密钥"
            @keyup.enter="submitCreate"
          />
        </el-form-item>
      </el-form>
      <div v-if="formErrors.length" class="form-errors">
        <el-icon><WarningFilled /></el-icon>
        {{ formErrors.join('；') }}
      </div>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitCreate">生成</el-button>
      </template>
    </el-dialog>

    <!-- Key reveal dialog (shown once) -->
    <el-dialog
      v-model="keyRevealVisible"
      title="API Key 已创建"
      width="520px"
      :close-on-click-modal="false"
      @close="closeReveal"
    >
      <div class="reveal-content">
        <el-alert type="warning" :closable="false" style="margin-bottom: 16px">
          请立即复制并妥善保存，此 Key 仅显示一次，关闭后将无法再次查看完整内容。
        </el-alert>
        <div class="reveal-key-box">
          <code class="reveal-key">{{ store.lastCreatedFullKey }}</code>
          <el-button type="primary" @click="copyKey(store.lastCreatedFullKey ?? '')">
            <el-icon><CopyDocument /></el-icon> 复制
          </el-button>
        </div>
      </div>
      <template #footer>
        <el-button type="primary" @click="closeReveal">我已保存，关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.key-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.key-code {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: var(--color-text-secondary);
  background: var(--color-bg-secondary);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  letter-spacing: 0.05em;
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

.reveal-key-box {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-active);
  border-radius: var(--radius-sm);
  padding: 12px 16px;
}

.reveal-key {
  flex: 1;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: var(--color-text-accent);
  word-break: break-all;
  letter-spacing: 0.05em;
}
</style>

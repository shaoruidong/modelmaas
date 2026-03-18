<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useTrainingStore } from '@/stores/training'
import { useModelStore } from '@/stores/models'
import StatusBadge from '@/components/common/StatusBadge.vue'
import { validateRequired } from '@/utils/validation'
import { mockDatasets } from '@/mock/data'
import type { TrainingConfig } from '@/types'

const trainingStore = useTrainingStore()
const modelStore = useModelStore()

// Dialog state
const dialogVisible = ref(false)
const currentStep = ref(0)
const detailDrawer = ref(false)
const selectedJob = ref<(typeof trainingStore.jobs)[0] | null>(null)
const formErrors = ref<string[]>([])

const form = reactive({
  name: '',
  baseModelId: '',
  baseModelName: '',
  datasetId: '',
  config: {
    epochs: 3,
    learningRate: 0.0001,
    batchSize: 16,
    method: 'SFT' as TrainingConfig['method'],
  },
})

const steps = ['选择基础模型', '选择数据集', '配置参数']

function openCreate() {
  Object.assign(form, {
    name: '',
    baseModelId: '',
    baseModelName: '',
    datasetId: '',
    config: { epochs: 3, learningRate: 0.0001, batchSize: 16, method: 'SFT' },
  })
  currentStep.value = 0
  formErrors.value = []
  dialogVisible.value = true
}

function nextStep() {
  formErrors.value = []
  if (currentStep.value === 0) {
    const errs = validateRequired({ 基础模型: form.baseModelId })
    if (errs.length) {
      formErrors.value = errs
      return
    }
  }
  if (currentStep.value === 1) {
    const errs = validateRequired({ 数据集: form.datasetId })
    if (errs.length) {
      formErrors.value = errs
      return
    }
  }
  currentStep.value++
}

function submitJob() {
  formErrors.value = []
  const errs = validateRequired({ 任务名称: form.name })
  if (errs.length) {
    formErrors.value = errs
    return
  }
  trainingStore.createJob({
    name: form.name,
    baseModelId: form.baseModelId,
    baseModelName: form.baseModelName,
    datasetId: form.datasetId,
    config: { ...form.config },
  })
  dialogVisible.value = false
}

function openDetail(job: (typeof trainingStore.jobs)[0]) {
  selectedJob.value = job
  detailDrawer.value = true
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleString('zh-CN', { hour12: false })
}
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">模型微调</h1>
      <el-button type="primary" @click="openCreate">
        <el-icon><Plus /></el-icon> 新建微调任务
      </el-button>
    </div>

    <!-- Jobs table -->
    <div class="maas-card" style="padding: 0; overflow: hidden">
      <el-table :data="trainingStore.jobs" style="width: 100%">
        <el-table-column prop="name" label="任务名称" min-width="160" />
        <el-table-column prop="baseModelName" label="基础模型" min-width="140" />
        <el-table-column label="训练方式" width="100">
          <template #default="{ row }">
            <el-tag size="small" effect="plain">{{ row.config.method }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <StatusBadge :status="row.status" />
          </template>
        </el-table-column>
        <el-table-column label="创建时间" min-width="160">
          <template #default="{ row }">{{ formatDate(row.createdAt) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button size="small" text type="primary" @click="openDetail(row)">详情</el-button>
            <el-popconfirm title="确认删除该任务？" @confirm="trainingStore.deleteJob(row.id)">
              <template #reference>
                <el-button size="small" text type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- Create dialog -->
    <el-dialog
      v-model="dialogVisible"
      title="新建微调任务"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-steps :active="currentStep" finish-status="success" style="margin-bottom: 28px">
        <el-step v-for="s in steps" :key="s" :title="s" />
      </el-steps>

      <!-- Step 0: Select base model -->
      <div v-if="currentStep === 0">
        <div class="step-grid">
          <div
            v-for="m in modelStore.models.filter((m) => m.category === 'text')"
            :key="m.id"
            class="select-card"
            :class="{ selected: form.baseModelId === m.id }"
            @click="form.baseModelId = m.id; form.baseModelName = m.name"
          >
            <div class="select-card-name">{{ m.name }}</div>
            <div class="select-card-sub">{{ m.provider }} · {{ m.parameterSize }}</div>
          </div>
        </div>
      </div>

      <!-- Step 1: Select dataset -->
      <div v-if="currentStep === 1">
        <div class="step-grid">
          <div
            v-for="ds in mockDatasets"
            :key="ds.id"
            class="select-card"
            :class="{ selected: form.datasetId === ds.id }"
            @click="form.datasetId = ds.id"
          >
            <div class="select-card-name">{{ ds.name }}</div>
            <div class="select-card-sub">
              {{ ds.type }} · {{ ds.recordCount.toLocaleString() }} 条
            </div>
          </div>
        </div>
      </div>

      <!-- Step 2: Config -->
      <div v-if="currentStep === 2">
        <el-form label-width="100px">
          <el-form-item label="任务名称" required>
            <el-input v-model="form.name" placeholder="请输入任务名称" />
          </el-form-item>
          <el-form-item label="训练方式">
            <el-select v-model="form.config.method" style="width: 100%">
              <el-option label="SFT（监督微调）" value="SFT" />
              <el-option label="DPO（直接偏好优化）" value="DPO" />
              <el-option label="RLHF（人类反馈强化学习）" value="RLHF" />
            </el-select>
          </el-form-item>
          <el-form-item label="训练轮数">
            <el-input-number v-model="form.config.epochs" :min="1" :max="20" />
          </el-form-item>
          <el-form-item label="学习率">
            <el-input v-model.number="form.config.learningRate" placeholder="0.0001" />
          </el-form-item>
          <el-form-item label="批次大小">
            <el-input-number v-model="form.config.batchSize" :min="1" :max="128" :step="8" />
          </el-form-item>
        </el-form>
      </div>

      <!-- Errors -->
      <div v-if="formErrors.length" class="form-errors">
        <el-icon><WarningFilled /></el-icon>
        {{ formErrors.join('；') }}
      </div>

      <template #footer>
        <el-button v-if="currentStep > 0" @click="currentStep--">上一步</el-button>
        <el-button v-if="currentStep < 2" type="primary" @click="nextStep">下一步</el-button>
        <el-button v-if="currentStep === 2" type="primary" @click="submitJob">提交任务</el-button>
      </template>
    </el-dialog>

    <!-- Detail drawer -->
    <el-drawer v-model="detailDrawer" title="任务详情" size="400px" v-if="selectedJob">
      <div class="drawer-content">
        <div class="info-row">
          <span>任务名称</span><span>{{ selectedJob.name }}</span>
        </div>
        <div class="info-row">
          <span>基础模型</span><span>{{ selectedJob.baseModelName }}</span>
        </div>
        <div class="info-row">
          <span>训练方式</span><span>{{ selectedJob.config.method }}</span>
        </div>
        <div class="info-row">
          <span>训练轮数</span><span>{{ selectedJob.config.epochs }}</span>
        </div>
        <div class="info-row">
          <span>学习率</span><span>{{ selectedJob.config.learningRate }}</span>
        </div>
        <div class="info-row">
          <span>批次大小</span><span>{{ selectedJob.config.batchSize }}</span>
        </div>
        <div class="info-row"><span>状态</span><StatusBadge :status="selectedJob.status" /></div>
        <div class="info-row">
          <span>创建时间</span><span>{{ formatDate(selectedJob.createdAt) }}</span>
        </div>

        <div style="margin-top: 24px">
          <div style="font-size: 13px; color: var(--color-text-muted); margin-bottom: 8px">
            训练进度
          </div>
          <el-progress
            :percentage="
              selectedJob.status === '已完成' ? 100 : selectedJob.status === '运行中' ? 65 : 0
            "
            :status="
              selectedJob.status === '失败'
                ? 'exception'
                : selectedJob.status === '已完成'
                  ? 'success'
                  : undefined
            "
          />
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<style scoped>
.step-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  max-height: 300px;
  overflow-y: auto;
}

.select-card {
  padding: 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.select-card:hover {
  border-color: var(--color-accent);
  background: var(--color-accent-light);
}

.select-card.selected {
  border-color: var(--color-accent);
  background: var(--color-accent-light);
  box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.2);
}

.select-card-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.select-card-sub {
  font-size: 11px;
  color: var(--color-text-muted);
  margin-top: 4px;
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

.drawer-content {
  padding: 8px 0;
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
</style>

export interface User {
  id: string
  username: string
  role: 'admin' | 'user'
}

export type ModelCategory = 'text' | 'vision' | 'audio' | 'multimodal' | 'embedding'

export interface Model {
  id: string
  name: string
  description: string
  category: ModelCategory
  tags: string[]
  provider: string
  parameterSize: string
  status: 'available' | 'deprecated'
  createdAt: string
}

export type TrainingStatus = '待运行' | '运行中' | '已完成' | '失败'

export interface TrainingConfig {
  epochs: number
  learningRate: number
  batchSize: number
  method: 'SFT' | 'DPO' | 'RLHF'
}

export interface TrainingJob {
  id: string
  name: string
  baseModelId: string
  baseModelName: string
  datasetId: string
  status: TrainingStatus
  createdAt: string
  finishedAt?: string
  config: TrainingConfig
}

export interface Dataset {
  id: string
  name: string
  description: string
  type: 'text' | 'image' | 'audio' | 'multimodal'
  size: number
  recordCount: number
  createdAt: string
}

export interface ApiKey {
  id: string
  name: string
  keyPrefix: string
  maskedKey: string
  status: 'active' | 'disabled'
  createdAt: string
  lastUsedAt?: string
}

export interface NavItem {
  key: string
  label: string
  icon: string
  path: string
  children?: NavItem[]
}

export interface MetricSummary {
  totalModels: number
  activeJobs: number
  apiCallsToday: number
  datasetCount: number
}

export interface AnalyticsData {
  dates: string[]
  apiCalls: number[]
  tokensConsumed: number[]
}

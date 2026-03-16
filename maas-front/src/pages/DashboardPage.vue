<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import MetricCard from '@/components/common/MetricCard.vue'
import { mockMetricSummary } from '@/mock/data'

const router = useRouter()
const metrics = ref(mockMetricSummary)

const toolchain = [
  {
    title: '选模型',
    subtitle: 'Model Selection',
    icon: 'Search',
    color: '#1677ff',
    desc: '支持多参数级别模型在线推理体验及测试',
    items: ['模型体验', '模型对比评测', '模型自主评测', '模型接口查看'],
    path: '/models',
  },
  {
    title: '改模型',
    subtitle: 'Model Modification',
    icon: 'Setting',
    color: '#7c3aed',
    desc: '支持模型训练、模型压缩及在线管理',
    items: [
      '支持预训练、SFT、DPO、RLHF等训练方式',
      '支持预训练检查点续训',
      '支持模型量化压缩',
      '支持模型自动操作和在线测试',
    ],
    path: '/fine-tuning',
  },
  {
    title: '用模型',
    subtitle: 'Model Usage',
    icon: 'Promotion',
    color: '#059669',
    desc: '支持大模型在线使用及原生应用创建',
    items: ['大模型在线使用', '原生应用搭建', '通用组件应用', '提示词工程'],
    path: '/inference',
  },
]

const announcements = [
  { time: '2024-03-15', text: '用户下单数据库升级：商品库、客管库、订单库 2.0版本上线' },
  {
    time: '2024-03-14',
    text: '新增模型列表刷新：新增套餐订单查看员工卡，支持用户业务员体内品及老客名称、服务内容、专属APIKEY、状态等信息',
  },
  {
    time: '2024-03-13',
    text: 'APIKEY管理升级：新增"院的客餐APIKLY"，支持用户订阅主套餐专属APIKEY及自定义APIKEY',
  },
  {
    time: '2024-03-12',
    text: '新增品及下单场景述房间，可以看客餐详况，常见问题等，下半部分体验体优化改善',
  },
]
</script>

<template>
  <div class="page-container">
    <!-- Hero banner -->
    <div class="hero-banner">
      <div class="hero-content">
        <h1 class="hero-title">
          释放 AI 无限潜能，<span class="gradient-text">重塑企业数智化未来</span>
        </h1>
        <p class="hero-desc">
          欢迎使用 MaaS 大模型平台。本平台为大模型工具平台，具备"选改用"一站式工具链。
          希望与您一同解锁无限创新可能，赋能千行百业。
        </p>
        <div class="hero-actions">
          <el-button type="primary" size="large" @click="router.push('/models')">
            立即开始 →
          </el-button>
          <el-button size="large" plain>查看文档</el-button>
        </div>
      </div>
      <div class="hero-visual">
        <div class="visual-card">
          <div class="visual-icon">🤖</div>
        </div>
      </div>
    </div>

    <!-- Metric cards -->
    <div class="section-title"><span class="section-bar"></span>核心指标监控</div>
    <div class="metrics-grid">
      <MetricCard
        title="模型广场"
        :value="metrics.totalModels"
        icon="Grid"
        color="linear-gradient(135deg,#1677ff,#06b6d4)"
        :trend="12"
      />
      <MetricCard
        title="我的模型"
        :value="metrics.activeJobs"
        icon="Cpu"
        color="linear-gradient(135deg,#7c3aed,#ec4899)"
      />
      <MetricCard
        title="模型评估"
        :value="0"
        icon="DataAnalysis"
        color="linear-gradient(135deg,#059669,#10b981)"
      />
      <MetricCard
        title="模型压缩"
        :value="0"
        icon="Compress"
        color="linear-gradient(135deg,#f59e0b,#ef4444)"
      />
      <MetricCard
        title="训练任务"
        :value="metrics.activeJobs"
        icon="Operation"
        color="linear-gradient(135deg,#ef4444,#f97316)"
      />
      <MetricCard
        title="数据集管理"
        :value="metrics.datasetCount"
        icon="FolderOpened"
        color="linear-gradient(135deg,#3b82f6,#6366f1)"
      />
    </div>

    <!-- Toolchain -->
    <div class="section-title"><span class="section-bar"></span>一站式工具链</div>
    <div class="toolchain-grid">
      <div
        v-for="tool in toolchain"
        :key="tool.title"
        class="tool-card"
        @click="router.push(tool.path)"
      >
        <div class="tool-header">
          <div>
            <div class="tool-title">
              {{ tool.title }} →
              <span class="tool-subtitle">{{ tool.subtitle }}</span>
            </div>
            <div class="tool-icon-wrap" :style="{ background: tool.color }">
              <el-icon size="20" color="#fff"><component :is="tool.icon" /></el-icon>
            </div>
          </div>
          <p class="tool-desc">{{ tool.desc }}</p>
        </div>
        <ul class="tool-items">
          <li v-for="item in tool.items" :key="item">{{ item }}</li>
        </ul>
      </div>
    </div>

    <!-- Announcements -->
    <div class="section-title"><span class="section-bar"></span>最新动态</div>
    <div class="announcements">
      <div v-for="ann in announcements" :key="ann.time" class="ann-item">
        <span class="ann-time">{{ ann.time }}</span>
        <span class="ann-text">{{ ann.text }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Hero */
.hero-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, rgba(22, 119, 255, 0.08) 0%, rgba(124, 58, 237, 0.08) 100%);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 40px;
  margin-bottom: var(--spacing-xl);
  overflow: hidden;
  position: relative;
}

.hero-banner::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(22, 119, 255, 0.12), transparent 70%);
  pointer-events: none;
}

.hero-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.4;
  margin-bottom: 12px;
}

.hero-desc {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.8;
  max-width: 480px;
  margin-bottom: 24px;
}

.hero-actions {
  display: flex;
  gap: 12px;
}

.hero-visual {
  flex-shrink: 0;
}

.visual-card {
  width: 120px;
  height: 120px;
  background: var(--gradient-primary);
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 56px;
  box-shadow: var(--shadow-glow);
  animation: float 4s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* Section title */
.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.section-bar {
  display: inline-block;
  width: 4px;
  height: 18px;
  background: var(--gradient-primary);
  border-radius: 2px;
}

/* Metrics */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

/* Toolchain */
.toolchain-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.tool-card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
}

.tool-card:hover {
  border-color: var(--color-border-active);
  box-shadow: var(--shadow-glow);
  transform: translateY(-2px);
}

.tool-header {
  margin-bottom: 16px;
}

.tool-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.tool-subtitle {
  font-size: 11px;
  color: var(--color-text-muted);
  font-weight: 400;
  margin-left: 8px;
}

.tool-icon-wrap {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.tool-desc {
  font-size: 12px;
  color: var(--color-text-secondary);
  line-height: 1.6;
}

.tool-items {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.tool-items li {
  font-size: 12px;
  color: var(--color-text-muted);
  padding-left: 12px;
  position: relative;
}

.tool-items li::before {
  content: '·';
  position: absolute;
  left: 0;
  color: var(--color-accent);
}

/* Announcements */
.announcements {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.ann-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 14px var(--spacing-lg);
  border-bottom: 1px solid var(--color-border);
  transition: background var(--transition-fast);
}

.ann-item:last-child {
  border-bottom: none;
}

.ann-item:hover {
  background: var(--color-bg-card-hover);
}

.ann-time {
  font-size: 12px;
  color: var(--color-text-muted);
  white-space: nowrap;
  flex-shrink: 0;
}

.ann-text {
  font-size: 13px;
  color: var(--color-text-secondary);
  line-height: 1.6;
}
</style>

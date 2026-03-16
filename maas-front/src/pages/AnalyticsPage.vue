<script setup lang="ts">
import { ref, computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import { TooltipComponent, LegendComponent } from 'echarts/components'
import type { EChartsOption } from 'echarts'
import LineChart from '@/components/charts/LineChart.vue'
import MetricCard from '@/components/common/MetricCard.vue'
import { mockAnalyticsData, mockModels } from '@/mock/data'

use([CanvasRenderer, PieChart, TooltipComponent, LegendComponent])

type Range = 'day' | 'week' | 'month'
const selectedRange = ref<Range>('week')

const rangeOptions: { label: string; value: Range }[] = [
  { label: '日', value: 'day' },
  { label: '周', value: 'week' },
  { label: '月', value: 'month' },
]

// Simulate different data per range
const rangeData = {
  day: {
    dates: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
    apiCalls: [1200, 800, 3400, 6800, 5200, 4100, 2300],
    tokens: [480000, 320000, 1360000, 2720000, 2080000, 1640000, 920000],
  },
  week: mockAnalyticsData,
  month: {
    dates: ['03-01', '03-05', '03-10', '03-15', '03-20', '03-25', '03-31'],
    apiCalls: [280000, 310000, 350000, 420000, 390000, 460000, 510000],
    tokens: [112000000, 124000000, 140000000, 168000000, 156000000, 184000000, 204000000],
  },
}

const currentData = computed(() => rangeData[selectedRange.value])

const totalApiCalls = computed(() => currentData.value.apiCalls.reduce((a, b) => a + b, 0))
const totalTokens = computed(() => currentData.value.tokens.reduce((a, b) => a + b, 0))

function formatTokens(n: number): string {
  if (n >= 1e8) return `${(n / 1e8).toFixed(1)}亿`
  if (n >= 1e4) return `${(n / 1e4).toFixed(0)}万`
  return n.toLocaleString()
}

// Pie chart for model usage
const pieOption = computed<EChartsOption>(() => ({
  backgroundColor: 'transparent',
  tooltip: {
    trigger: 'item',
    backgroundColor: '#1a2235',
    borderColor: 'rgba(22,119,255,0.3)',
    textStyle: { color: '#e2e8f0', fontSize: 12 },
    formatter: '{b}: {c} 次 ({d}%)',
  },
  legend: {
    orient: 'vertical',
    right: 16,
    top: 'center',
    textStyle: { color: '#94a3b8', fontSize: 12 },
  },
  series: [
    {
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['38%', '50%'],
      data: mockModels.slice(0, 6).map((m, i) => ({
        name: m.name,
        value: Math.floor(Math.random() * 10000 + 1000),
        itemStyle: {
          color: ['#1677ff', '#7c3aed', '#059669', '#f59e0b', '#ef4444', '#06b6d4'][i],
        },
      })),
      label: { show: false },
      emphasis: {
        itemStyle: { shadowBlur: 10, shadowColor: 'rgba(22,119,255,0.4)' },
      },
    },
  ],
}))
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">统计看板</h1>
      <div class="range-tabs">
        <button
          v-for="r in rangeOptions"
          :key="r.value"
          class="range-tab"
          :class="{ active: selectedRange === r.value }"
          @click="selectedRange = r.value"
        >
          {{ r.label }}
        </button>
      </div>
    </div>

    <!-- Summary cards -->
    <div class="summary-grid">
      <MetricCard
        title="API 调用总量"
        :value="totalApiCalls.toLocaleString()"
        icon="DataLine"
        color="linear-gradient(135deg,#1677ff,#06b6d4)"
        :trend="8"
      />
      <MetricCard
        title="Token 消耗总量"
        :value="formatTokens(totalTokens)"
        icon="Coin"
        color="linear-gradient(135deg,#7c3aed,#ec4899)"
        :trend="12"
      />
      <MetricCard
        title="活跃模型数"
        :value="mockModels.filter((m) => m.status === 'available').length"
        icon="Cpu"
        color="linear-gradient(135deg,#059669,#10b981)"
      />
      <MetricCard
        title="平均响应时间"
        value="238ms"
        icon="Timer"
        color="linear-gradient(135deg,#f59e0b,#ef4444)"
        :trend="-5"
      />
    </div>

    <!-- Charts row -->
    <div class="charts-row">
      <!-- API calls trend -->
      <div class="chart-card maas-card">
        <div class="chart-title">API 调用趋势</div>
        <LineChart
          :dates="currentData.dates"
          :series="[{ name: 'API 调用量', data: currentData.apiCalls, color: '#1677ff' }]"
          height="240px"
        />
      </div>

      <!-- Token consumption trend -->
      <div class="chart-card maas-card">
        <div class="chart-title">Token 消耗趋势</div>
        <LineChart
          :dates="currentData.dates"
          :series="[
            {
              name: 'Token 消耗',
              data: currentData.tokens.map((t) => Math.round(t / 10000)),
              color: '#7c3aed',
            },
          ]"
          height="240px"
        />
      </div>
    </div>

    <!-- Model usage pie -->
    <div class="maas-card">
      <div class="chart-title">模型使用分布</div>
      <v-chart :option="pieOption" style="height: 300px; width: 100%" autoresize />
    </div>
  </div>
</template>

<style scoped>
.range-tabs {
  display: flex;
  gap: 4px;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 3px;
}

.range-tab {
  padding: 5px 16px;
  border-radius: 4px;
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.range-tab.active {
  background: var(--color-accent);
  color: #fff;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.chart-card {
  min-height: 300px;
}

.chart-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}
</style>

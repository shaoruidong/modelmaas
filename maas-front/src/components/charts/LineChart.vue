<script setup lang="ts">
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import type { EChartsOption } from 'echarts'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent])

const props = defineProps<{
  dates: string[]
  series: { name: string; data: number[]; color?: string }[]
  height?: string
}>()

const option = computed<EChartsOption>(() => ({
  backgroundColor: 'transparent',
  tooltip: {
    trigger: 'axis',
    backgroundColor: '#1a2235',
    borderColor: 'rgba(22,119,255,0.3)',
    textStyle: { color: '#e2e8f0', fontSize: 12 },
  },
  legend: {
    textStyle: { color: '#94a3b8', fontSize: 12 },
    top: 0,
  },
  grid: { left: 16, right: 16, bottom: 8, top: 36, containLabel: true },
  xAxis: {
    type: 'category',
    data: props.dates,
    axisLine: { lineStyle: { color: 'rgba(255,255,255,0.08)' } },
    axisLabel: { color: '#64748b', fontSize: 11 },
    splitLine: { show: false },
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false },
    axisLabel: { color: '#64748b', fontSize: 11 },
    splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } },
  },
  series: props.series.map((s) => ({
    name: s.name,
    type: 'line',
    data: s.data,
    smooth: true,
    symbol: 'circle',
    symbolSize: 6,
    lineStyle: { width: 2, color: s.color ?? '#1677ff' },
    itemStyle: { color: s.color ?? '#1677ff' },
    areaStyle: {
      color: {
        type: 'linear',
        x: 0,
        y: 0,
        x2: 0,
        y2: 1,
        colorStops: [
          { offset: 0, color: (s.color ?? '#1677ff') + '40' },
          { offset: 1, color: (s.color ?? '#1677ff') + '00' },
        ],
      },
    },
  })),
}))
</script>

<template>
  <v-chart :option="option" :style="{ height: height ?? '280px', width: '100%' }" autoresize />
</template>

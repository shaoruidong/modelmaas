import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Dataset } from '@/types'
import { mockDatasets } from '@/mock/data'

export const useDatasetStore = defineStore('datasets', () => {
  const datasets = ref<Dataset[]>([...mockDatasets])

  function createDataset(
    data: Omit<Dataset, 'id' | 'createdAt' | 'size' | 'recordCount'>,
  ): Dataset {
    const ds: Dataset = {
      id: `ds${Date.now()}`,
      ...data,
      size: 0,
      recordCount: 0,
      createdAt: new Date().toISOString(),
    }
    datasets.value.unshift(ds)
    return ds
  }

  function deleteDataset(id: string) {
    datasets.value = datasets.value.filter((d) => d.id !== id)
  }

  return { datasets, createDataset, deleteDataset }
})

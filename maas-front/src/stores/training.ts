import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { TrainingJob, TrainingConfig } from '@/types'
import { mockTrainingJobs } from '@/mock/data'

export const useTrainingStore = defineStore('training', () => {
  const jobs = ref<TrainingJob[]>([...mockTrainingJobs])

  function createJob(data: {
    name: string
    baseModelId: string
    baseModelName: string
    datasetId: string
    config: TrainingConfig
  }): TrainingJob {
    const job: TrainingJob = {
      id: `tj${Date.now()}`,
      ...data,
      status: '待运行',
      createdAt: new Date().toISOString(),
    }
    jobs.value.unshift(job)
    return job
  }

  function deleteJob(id: string) {
    jobs.value = jobs.value.filter((j) => j.id !== id)
  }

  return { jobs, createJob, deleteJob }
})

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Model, ModelCategory } from '@/types'
import { mockModels } from '@/mock/data'
import { filterModelsByKeyword, filterModelsByCategory } from '@/utils/filter'

export const useModelStore = defineStore('models', () => {
  const models = ref<Model[]>(mockModels)
  const searchKeyword = ref('')
  const selectedCategory = ref<ModelCategory | ''>('')
  const loading = ref(false)

  const filteredModels = computed(() => {
    let result = filterModelsByKeyword(models.value, searchKeyword.value)
    result = filterModelsByCategory(result, selectedCategory.value)
    return result
  })

  return { models, searchKeyword, selectedCategory, loading, filteredModels }
})

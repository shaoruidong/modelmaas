import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ApiKey } from '@/types'
import { mockApiKeys } from '@/mock/data'
import { generateApiKey, maskApiKey } from '@/utils/validation'

export const useApiKeyStore = defineStore('apikeys', () => {
  const apiKeys = ref<ApiKey[]>([...mockApiKeys])
  const lastCreatedFullKey = ref<string | null>(null)

  function createApiKey(name: string): ApiKey {
    const fullKey = generateApiKey()
    lastCreatedFullKey.value = fullKey
    const key: ApiKey = {
      id: `ak${Date.now()}`,
      name,
      keyPrefix: fullKey.slice(0, 8),
      maskedKey: maskApiKey(fullKey),
      status: 'active',
      createdAt: new Date().toISOString(),
    }
    apiKeys.value.unshift(key)
    return key
  }

  function deleteApiKey(id: string) {
    apiKeys.value = apiKeys.value.filter((k) => k.id !== id)
  }

  function clearLastKey() {
    lastCreatedFullKey.value = null
  }

  return { apiKeys, lastCreatedFullKey, createApiKey, deleteApiKey, clearLastKey }
})

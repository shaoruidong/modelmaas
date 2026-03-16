import type { Model, ModelCategory } from '@/types'

export function filterModelsByKeyword(models: Model[], keyword: string): Model[] {
  if (!keyword.trim()) return models
  const lower = keyword.toLowerCase()
  return models.filter(
    (m) => m.name.toLowerCase().includes(lower) || m.description.toLowerCase().includes(lower),
  )
}

export function filterModelsByCategory(models: Model[], category: ModelCategory | ''): Model[] {
  if (!category) return models
  return models.filter((m) => m.category === category)
}

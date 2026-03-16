export function validateRequired(fields: Record<string, unknown>): string[] {
  const errors: string[] = []
  for (const [key, value] of Object.entries(fields)) {
    if (value === null || value === undefined || String(value).trim() === '') {
      errors.push(`${key} 不能为空`)
    }
  }
  return errors
}

export function maskApiKey(fullKey: string): string {
  if (fullKey.length <= 8) return '•'.repeat(fullKey.length)
  return fullKey.slice(0, 8) + '•'.repeat(Math.max(fullKey.length - 8, 24))
}

export function generateApiKey(): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let key = 'sk-'
  for (let i = 0; i < 48; i++) {
    key += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return key
}

export function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`
}

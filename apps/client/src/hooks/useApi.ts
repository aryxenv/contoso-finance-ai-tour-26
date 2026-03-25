import { useEffect, useState } from 'react'
import { apiClient } from '../api/client'

interface UseApiResult<T> {
  data: T | null
  error: Error | null
  loading: boolean
}

export function useApi<T>(endpoint: string): UseApiResult<T> {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false

    async function fetchData() {
      try {
        setLoading(true)
        const result = await apiClient<T>(endpoint)
        if (!cancelled) setData(result)
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err : new Error(String(err)))
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    fetchData()
    return () => { cancelled = true }
  }, [endpoint])

  return { data, error, loading }
}

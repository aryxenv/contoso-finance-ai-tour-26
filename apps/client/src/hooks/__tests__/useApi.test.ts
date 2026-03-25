import { renderHook, waitFor } from '@testing-library/react'
import { useApi } from '../useApi'
import { apiClient } from '../../api/client'

vi.mock('../../api/client', () => ({
  apiClient: vi.fn(),
}))

describe('useApi', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('starts in loading state', () => {
    vi.mocked(apiClient).mockReturnValue(new Promise(() => {})) // never resolves

    const { result } = renderHook(() => useApi('/api/test'))

    expect(result.current.loading).toBe(true)
    expect(result.current.data).toBeNull()
    expect(result.current.error).toBeNull()
  })

  it('returns data on successful fetch', async () => {
    const mockData = { id: 1, name: 'Test' }
    vi.mocked(apiClient).mockResolvedValue(mockData)

    const { result } = renderHook(() => useApi('/api/items'))

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.data).toEqual(mockData)
    expect(result.current.error).toBeNull()
  })

  it('returns error on failed fetch', async () => {
    vi.mocked(apiClient).mockRejectedValue(new Error('Network error'))

    const { result } = renderHook(() => useApi('/api/fail'))

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.error).toBeInstanceOf(Error)
    expect(result.current.error?.message).toBe('Network error')
    expect(result.current.data).toBeNull()
  })

  it('calls apiClient with the correct endpoint', async () => {
    vi.mocked(apiClient).mockResolvedValue({})

    renderHook(() => useApi('/api/billing'))

    await waitFor(() => {
      expect(apiClient).toHaveBeenCalledWith('/api/billing')
    })
  })
})

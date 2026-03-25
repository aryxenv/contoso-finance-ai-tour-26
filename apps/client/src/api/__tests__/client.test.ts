import { apiClient } from '../client'

describe('apiClient', () => {
  const originalFetch = globalThis.fetch

  beforeEach(() => {
    globalThis.fetch = vi.fn()
  })

  afterEach(() => {
    globalThis.fetch = originalFetch
  })

  it('builds the correct URL from endpoint', async () => {
    const mockResponse = { ok: true, json: () => Promise.resolve({ id: 1 }) }
    vi.mocked(globalThis.fetch).mockResolvedValue(mockResponse as Response)

    await apiClient('/api/test')

    expect(globalThis.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/test',
      expect.objectContaining({
        headers: expect.objectContaining({ 'Content-Type': 'application/json' }),
      }),
    )
  })

  it('returns parsed JSON on successful response', async () => {
    const data = { id: 1, name: 'Test' }
    const mockResponse = { ok: true, json: () => Promise.resolve(data) }
    vi.mocked(globalThis.fetch).mockResolvedValue(mockResponse as Response)

    const result = await apiClient('/api/items')

    expect(result).toEqual(data)
  })

  it('throws an error on non-ok response', async () => {
    const mockResponse = { ok: false, status: 404, json: () => Promise.resolve({}) }
    vi.mocked(globalThis.fetch).mockResolvedValue(mockResponse as Response)

    await expect(apiClient('/api/missing')).rejects.toThrow('API error: 404')
  })

  it('passes custom options through to fetch', async () => {
    const mockResponse = { ok: true, json: () => Promise.resolve({}) }
    vi.mocked(globalThis.fetch).mockResolvedValue(mockResponse as Response)

    await apiClient('/api/data', { method: 'POST', body: JSON.stringify({ x: 1 }) })

    expect(globalThis.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/data',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ x: 1 }),
      }),
    )
  })
})
